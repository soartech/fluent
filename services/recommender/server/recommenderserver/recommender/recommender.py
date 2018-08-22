import datetime
from itertools import filterfalse
from typing import List, Type, Optional

from activity_index_client.models import LearningActivity
from cass_client.models import Competency
from cass_graph_client.cass_graph import CassGraph
from learner_inferences_client.models import Learner, Goal, MasteryEstimate
from recommenderserver.xapi_wrapper import XApiStatement, XAPISender
from recommenderserver.config import Config, CassConfig, LoggingLRSConfig
from recommenderserver.models import *
from recommenderserver.recommender import utils
from recommenderserver.recommender.config import MandatoryAssignmentMakerConfig, RowStrategyConfig
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.row_strategies import CompetencyRowStrategy, ActivityRowStrategy
from recommenderserver.recommender.utils import MagicStrings, filter_debug_activities, filter_pretest_activities, \
    filter_posttest_activities
from recommenderserver.recommender.row_strategies import TimeForCapstone
import json


NUM_LEARNER_PATCH_RETRIES=20

class MandatoryAssignmentMaker(object):
    def __init__(self, learner: Learner, etag: str, query_cacher: QueryCacher, cass_graph: CassGraph):
        self.learner = learner
        self.etag = etag
        self.query_cacher = query_cacher
        self.cass_graph = cass_graph

    def get_mandatory_assignment(self) -> Optional[Recommendation]:
        if MandatoryAssignmentMakerConfig.SELF_REPORT:
            # Self report
            self_report = self._get_required_self_report()
            if self_report is not None: return self._assignment(self_report)

        if MandatoryAssignmentMakerConfig.FORMATIVE_ASSESSMENT:
            # Check on learning
            check_on_learning_assessment = self._get_required_check_on_learning_assessment()
            if check_on_learning_assessment is not None: return self._assignment(check_on_learning_assessment)

        if MandatoryAssignmentMakerConfig.METACOGNITIVE_PROMPT:
            # Metacognitive Prompt
            metacognitive_prompt = self._get_metacognitive_prompt()
            if metacognitive_prompt is not None: return self._assignment(metacognitive_prompt)

        if MandatoryAssignmentMakerConfig.TLO_UNIT_ASSESSMENT:
            # Unit assessment post-test
            unit_assessment = self._get_unit_assessment()
            if unit_assessment is not None: return self._assignment(unit_assessment)
        else:
            # Find out if all ELOs in the current TLO are held, and update the TLO mastery estimate if necessary.
            self._update_tlo_if_necessary()

        return None

    def _get_metacognitive_prompt(self) -> Optional[LearningActivity]:
        # Get the metacognitive prompt if the learner has mastered an ELO and
        # they have not seen the metacognitive prompt before.
        last_activity = self._get_last_activity()
        if last_activity is not None:
            aligned_elo = utils.get_aligned_elo(last_activity)
            if aligned_elo is not None and utils.get_elo_mastery_estimate(aligned_elo, self.learner) == MagicStrings.MasteryEstimates.HELD:
                metacognitive_prompt = self._get_metacognitive_prompt_for_elo(aligned_elo)
                if metacognitive_prompt is not None and not self._has_learner_taken_activity(metacognitive_prompt):
                    return metacognitive_prompt

        return None

    def _has_learner_taken_activity(self, activity: LearningActivity):
        for attempt in self.learner.activity_attempt_counters:
            if attempt.activity_id == activity.identifier:
                return True
        return False

    def _get_metacognitive_prompt_for_elo(self, elo_id: str) -> Optional[LearningActivity]:
        all_activities = self.query_cacher.get_activities()
        for activity in all_activities:
            activity_elo = utils.get_aligned_elo(activity)
            if utils.target_url_equals_competency(activity_elo, elo_id) and activity.learning_resource_type == MagicStrings.LearningResourceTypes.METACOGNITIVE_PROMPT:
                return activity
        return None

    def _get_required_check_on_learning_assessment(self) -> Optional[LearningActivity]:
        last_5_activities = utils.last_n_activities_attempted(self.learner.activity_attempt_counters, 5,
                                                              self.query_cacher)
        for activity in last_5_activities:
            if utils.educational_use_in_activity(activity, MagicStrings.EducationalUses.SELF_REPORT):
                continue
            if utils.educational_use_in_activity(activity, MagicStrings.EducationalUses.ASSESSES):
                return None

            assessment_id = utils.get_check_on_learning_assessment_acitivity_id(activity)
            if assessment_id is not None:
                return self.query_cacher.get_activity(utils.mongo_id_from_url(assessment_id))
        return None

    def _assignment(self, assignment: LearningActivity) -> Recommendation:
        return Recommendation(type='Recommendation', timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc), learner=self.learner.identifier,
                              assignment=self.assignment_activity(assignment), recommendations=None)

    def _get_required_self_report(self) -> Optional[LearningActivity]:
        last_5_activities = utils.last_n_activities_attempted(self.learner.activity_attempt_counters, 5, self.query_cacher)

        # Self report required if user has not yet taken a self report after having taken a regular activity
        for activity in last_5_activities:
            if utils.educational_use_in_activity(activity, MagicStrings.EducationalUses.SELF_REPORT):
                return None
            if not utils.educational_use_in_activity(activity, MagicStrings.EducationalUses.ASSESSES):
                return self.query_cacher.get_self_report()
        return None

    def assignment_activity(self, activity):
        return RecommendedActivity(activity_id=activity.identifier, tokens=1)

    def _update_tlo_if_necessary(self):
        current_tlo = self._get_current_tlo()
        elos = self._get_elos_by_tlo(current_tlo)
        if self._all_elos_held(elos):
            for estimate in self.learner.mastery_estimates:
                if estimate.competency_id == current_tlo.id:
                    if estimate.mastery != MagicStrings.MasteryEstimates.HELD:
                        # Update mastery estimate for TLO to held.
                        self._update_learner_mastery_estimate(estimate, MagicStrings.MasteryEstimates.HELD)
                        pass
                    break

    def _update_learner_mastery_estimate(self, estimate_to_update: MasteryEstimate, mastery: str):
        estimate_to_update.mastery = mastery
        estimate_to_update.timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        for i, estimate in enumerate(self.learner.mastery_estimates):
            if estimate.competency_id == estimate_to_update.competency_id:
                self.learner.past_mastery_estimates.append(estimate)
                self.learner.mastery_estimates[i] = estimate_to_update

        for i in range(NUM_LEARNER_PATCH_RETRIES):
            # TODO - Competency Attempt Counters should NOT be a required field - would help avoid race conditions.
            learner_patch = Learner(name=self.learner.name, identifier=self.learner.identifier,
                                    context=self.learner.context, type=self.learner.type,
                                    competency_attempt_counters=self.learner.competency_attempt_counters,
                                    past_mastery_estimates=self.learner.past_mastery_estimates,
                                    mastery_estimates=self.learner.mastery_estimates)

            try:
                self.query_cacher.update_learner(self.learner.identifier, self.etag, learner_patch)
                break
            except:
                self.learner, self.etag = self.query_cacher.get_learner(self.learner.identifier, force_update=True)

            if i == NUM_LEARNER_PATCH_RETRIES-1:
                utils.print_with_time('WARN: Failed to update mastery estimates for learner {} after {} tries'.format(
                    self.learner.identifier, NUM_LEARNER_PATCH_RETRIES
                ))

    def _get_unit_assessment(self) -> Optional[LearningActivity]:
        # Gets the unit assessment for an TLO Activity group if it exists and is necessary.

        # Get the most recent TLO
        current_tlo = self._get_current_tlo()
        if not self._failed_unit_assessment_recently(current_tlo.id):
            # Get all ELOs from the CASS mapping that relate to the TLO
            elos = self._get_elos_by_tlo(current_tlo)

            if self._all_elos_held(elos):
                return self._get_unit_assessment_tlo_id(current_tlo.id)

        return None

    def _all_elos_held(self, elos: List[Competency]):
        elo_check = {
            elo.id: {
                'found': False,
                'mastery': MagicStrings.MasteryEstimates.UNKNOWN
            }
            for elo in elos
        }

        for estimate in self.learner.mastery_estimates:
            if estimate.competency_id in elo_check:
                elo_check[estimate.competency_id]['found'] = True
                elo_check[estimate.competency_id]['mastery'] = estimate.mastery

        found_bool = set([elo['found'] for elo in elo_check.values()])
        masteries = set([elo['mastery'] for elo in elo_check.values()])

        # Check if the learner has a "held" mastery estimate for all ELOs.
        return found_bool == {True} and masteries == {MagicStrings.MasteryEstimates.HELD}

    def _failed_unit_assessment_recently(self, tlo_id: str):
        # Checks to see if the unit assessment was failed within the past 3 attempts.
        activities = utils.last_n_activities_attempted(self.learner.activity_attempt_counters, 3, self.query_cacher)
        for activity in activities:
            if utils.tlo_in_activity(tlo_id, activity) and activity.learning_resource_type == MagicStrings.LearningResourceTypes.UNIT_ASSESSMENT:
                return True

        return False

    def _get_unit_assessment_tlo_id(self, tlo_id: str) -> Optional[LearningActivity]:
        activities = self.query_cacher.get_activities()
        for activity in activities:
            if activity.learning_resource_type == MagicStrings.LearningResourceTypes.UNIT_ASSESSMENT:
                for alignment in activity.educational_alignment:
                    if alignment.target_url == tlo_id:
                        return activity
        return None

    def _get_last_activity(self) -> Optional[LearningActivity]:
        return self.query_cacher.get_activity(
            utils.mongo_id_from_url(utils.get_last_activity_url_identifier(self.learner)))


    def _get_next_elo(self, elo: Competency) -> Optional[Competency]:
        competency = self.cass_graph.get_next_in_chain(elo)
        if competency.dctermstype == MagicStrings.DC_TERM_TYPES.ELO:
            return competency

        return None

    def _get_current_tlo(self) -> Optional[Competency]:
        tlo = self.cass_graph.get_first_top_level_competency()

        while tlo is not None:
            found = False
            for estimate in self.learner.mastery_estimates:
                if estimate.competency_id == tlo.id:
                    if estimate.mastery != MagicStrings.MasteryEstimates.HELD and estimate.mastery != MagicStrings.MasteryEstimates.FORGOT:
                        return tlo
                    else:
                        found = True
                        break
            if not found:
                return tlo

            tlo = self.cass_graph.get_next_neighbor(tlo)

        return None

    def _get_elos_by_tlo(self, tlo: Competency) -> List[Competency]:
        return self.cass_graph.get_competency_chain(tlo)

    def _unit_assessment_passed(self, tlo: Competency) -> bool:
        for estimate in self.learner.mastery_estimates:
            if estimate.competency_id == tlo.id:
                if estimate.mastery == MagicStrings.MasteryEstimates.HELD:
                    return True
                else:
                    return False

        return False


class Recommender(object):
    def __init__(self, learner: Learner, etag: str, query_cacher: QueryCacher,
                 elo_row_strategy_classes: List[Type[CompetencyRowStrategy]],
                 activity_row_strategy_classes: List[Type[ActivityRowStrategy]],
                 not_enough_content_elo_row_strategy_classes: List[Type[CompetencyRowStrategy]],
                 not_enough_content_activity_row_strategy_classes: List[Type[ActivityRowStrategy]],
                 cass_graph: CassGraph, min_content_threshold: int, filter_locked: bool, deduplicate_rows=False,
                 use_prerequisties=True, focus_competencies=False):
        self.query_cacher = query_cacher
        self.learner = learner
        self.etag = etag
        self.cass_graph = cass_graph
        self.focus_competencies = focus_competencies
        self.logic_steps = list()
        self.send_log_to_lrs = False
        self.send_log_to_file = True

        self.logic_steps.append("[INPUT] Learner has goal(s) with competency ids: {}".format([str(goal.competency_id) for goal in learner.goals]))
        self.logic_steps.append("[INPUT] Learner has mastery probabilities of: {}".format([json.dumps({'competencyId': mp.competency_id,
                                                                                                'probability': mp.probability,
                                                                                                'source': mp.source,
                                                                                                'timestamp': mp.timestamp.isoformat()})
                                                                                            for mp in learner.mastery_probabilities]))

        if use_prerequisties:
            utils.print_with_time("Using prerequisites")
            self.logic_steps.append("Using prerequisites")
            if self.focus_competencies:
                self.logic_steps.append("Using competency focus")
            else:
                self.logic_steps.append("Not using competency focus")
            self.active_elos = utils.get_goals_and_subgoals_using_prequisites(learner, cass_graph, return_all=(not self.focus_competencies))
            self.logic_steps.append("Active ELOs are set to: {}".format(str([elo.id for elo in self.active_elos])))
        else:
            utils.print_with_time("Not using prerequisites")
            self.logic_steps.append("Not using Prerequisites")
            self.active_elos = utils.get_goals_and_subgoals(learner, cass_graph)

        #START: Temporary debug logging code

        utils.print_with_time('Info: BEGIN fetching prereqs or subgoals for learner={}'.format(learner.name))
        utils.print_with_time('Info: Learner has goal(s) with competency ids:\n\t{}'.format(
            [str(goal.competency_id) for goal in learner.goals]
        ))

        learner_goal_competencies = []
        for goal in learner.goals:
            competency = cass_graph.get_obj_by_id(goal.competency_id)
            if competency is not None:
                learner_goal_competencies.append(competency)
            else:
                utils.print_with_time('Info: Unable to find learner goal with competency id={} in framework'.format(goal.competency_id))

        utils.print_with_time('Info: Learner has retrieved competency objects for learner goal competencies:\n\t{}'.format(
            [str(competency.ceasncoded_notation) + ':' + competency.id for competency in learner_goal_competencies]
        ))
        utils.print_with_time('Info: Making recommendations for competencies:\n\t{}'.format(
            [str(active_elo.ceasncoded_notation) + ':' + active_elo.id for active_elo in self.active_elos]
        ))
        utils.print_with_time('Info: END fetching prereqs or subgoals for learner={}'.format(learner.name))
        #END: Temporary debug logging code

        utils.print_with_time('Info: START Not enough content')
        # Use different strategies if there is not enough content
        if RowStrategyConfig.CHECK_FOR_TOO_FEW_ACTIVITIES:
            if self._not_enough_content(self.active_elos, min_content_threshold):
                utils.print_with_time("Not enough content")
                self.logic_steps.append("Determined there is not enough content to recommend (should be deprecated)")
                elo_row_strategy_classes = not_enough_content_elo_row_strategy_classes
                activity_row_strategy_classes = not_enough_content_activity_row_strategy_classes
        utils.print_with_time('INFO: END Not enough content')

        utils.print_with_time('INFO: START INIT COMPETENCY ROW STRATEGIES')
        self.elo_row_strategies = [
            row_strategy(learner=self.learner, query_cacher=self.query_cacher, cass_graph=cass_graph,
                         filter_locked=filter_locked)
            for row_strategy in elo_row_strategy_classes]
        utils.print_with_time('INFO: END init competency row strategies')

        self.activity_row_strategies = [
            row_strategy(learner=self.learner, query_cacher=self.query_cacher, cass_graph=cass_graph,
                         filter_locked=filter_locked
            ) for row_strategy in activity_row_strategy_classes]
        self.deduplicate_rows = deduplicate_rows

        self.logic_steps.append("{} row strategies have been initialized.".format(len(self.activity_row_strategies)+len(self.elo_row_strategies)))

    def get_recommendation(self) -> Recommendation:
        utils.print_with_time("Info: Instantiating Rows")
        rows = self._instantiate_all_rows()
        utils.print_with_time("Info: END Instantiating Rows")

        utils.print_with_time("Info: START Capstone check.")
        capstone_rows = self.get_capstone_if_able()
        for row in capstone_rows:
            rows.append(row)
        utils.print_with_time("Info: END Capstone check.")
        if self.deduplicate_rows:
            self.logic_steps.append("Deduplicated rows")
            self._deduplicate(rows)

        try:
            xapi_sender = XAPISender(base_url='http://' + LoggingLRSConfig.BASE_URL,
                                     x_experience_version=LoggingLRSConfig.X_EXPERIENCE_VERSION,
                                     basic_auth_user=LoggingLRSConfig.CLIENT_USR,
                                     basic_auth_pwd=LoggingLRSConfig.CLIENT_PWD)

            produced_statement = XApiStatement(actor_name=self.learner.identifier,
                                             account_name=self.learner.identifier,
                                             agent_url_id=Config.LEARNER_INFERENCE_BASE_URL + '/' + self.learner.identifier,
                                             verb_name="produced",
                                             object={"objectType": "Activity",
                                                     "definition": {
                                                         "name": {
                                                             "en": "Recommendation"
                                                         }
                                                     },
                                                     'id': Config.RECOMMENDER_URL
                                                     },
                                             context_extensions= {
                                                 Config.RECOMMENDER_URL+"/logic": self.logic_steps
                                             }
                                             )

            if self.send_log_to_lrs:
                response = xapi_sender.statements_post(produced_statement)
            if self.send_log_to_file:
                utils.print_with_time_split("{}".format(json.dumps(produced_statement.statement)), 'XAPI LOG')

            utils.print_with_time("Info: Logging statement sent.")
        except Exception as e:
            utils.print_with_time('WARN: the following error occurred when trying to send to the logging LRS: {}'.format(e.args))

        return Recommendation(type="Recommendation", timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc),
                              learner=utils.mongo_id_from_url(self.learner.identifier), assignment=None,
                              recommendations=rows)


    def get_capstone_if_able(self):
        rows = []
        for goal_obj in self.learner.goals:
            goal = self.cass_graph.get_obj_by_id(goal_obj.competency_id)
            parent = self.cass_graph.get_parent_competency(goal)

            while parent is not None:
                goal = parent
                parent = self.cass_graph.get_parent_competency(goal)

            elo_activities = self.query_cacher.get_activities_for_elo(goal.id)
            capstone_row_strategy = TimeForCapstone(self.learner, self.query_cacher, self.cass_graph, filter_locked=False, filter_capstone=False)
            competencies_to_instantiate = capstone_row_strategy.can_instantiate([goal])
            for competency in competencies_to_instantiate:
                row = capstone_row_strategy.instantiate_row(competency, elo_activities)
                if row is not None:
                    rows.append(row)

        if len(rows) > 0:
            self.logic_steps.append("Capstone recommended.")
        else:
            self.logic_steps.append("Capstone NOT recommended.")

        return rows


    def _instantiate_all_rows(self) -> List[RecommendationRow]:
        rows = list() # type: List[RecommendationRow]

        #self._update_learner_goals(self.active_elos)
        for row_strategy in self.elo_row_strategies:
            utils.print_with_time("Info: START Can_instantiate for: {}".format(row_strategy.__class__.__name__))
            elos_that_can_be_instantiated = row_strategy.can_instantiate(self.active_elos)
            self.logic_steps.append("Competencies that can be instantiated with {} competency row strategy: {}".format(row_strategy.__class__.__name__, str([comp.id for comp in elos_that_can_be_instantiated])))
            utils.print_with_time("Info: END can_instantiate for: {}".format(row_strategy.__class__.__name__))
            #TODO: ELO balancing can be applied here before instantiation
            for elo in elos_that_can_be_instantiated:
                utils.print_with_time("Info: START instantiate row for: {}".format(row_strategy.__class__.__name__))
                elo_activities = self.query_cacher.get_activities_for_elo(elo.id)

                row = row_strategy.instantiate_row(elo, elo_activities)
                rows.append(row)

                if row is None:
                    self.logic_steps.append("Row strategy {} for competency {} has no activities.".format(row_strategy.__class__.__name__, elo.id))
                else:
                    self.logic_steps.append(
                        "Row strategy {} for competency {} returned {} activities".format(row_strategy.__class__.__name__, elo.id, len(row.activities)))

                utils.print_with_time("Info: END instantiate row for: {}".format(row_strategy.__class__.__name__))
        for row_strategy in self.activity_row_strategies:
            utils.print_with_time("Info: START Can_instantiate for: {}".format(row_strategy.__class__.__name__))
            objs_that_can_be_instantiated = row_strategy.can_instantiate()
            try:
                self.logic_steps.append("Objects that can be instantiated with {} activity row strategy: {}".format(row_strategy.__class__.__name__, str([obj.identifier for obj in objs_that_can_be_instantiated])))
            except Exception:
                self.logic_steps.append("Objects that can be instantiated with {} activity row strategy: {}".format(row_strategy.__class__.__name__, str(objs_that_can_be_instantiated)))
            utils.print_with_time("Info: END can_instantiate for: {}".format(row_strategy.__class__.__name__))
            for obj in objs_that_can_be_instantiated:
                utils.print_with_time("Info: START instantiate row for: {}".format(row_strategy.__class__.__name__))

                row = row_strategy.instantiate_row(self.active_elos, obj)
                rows.append(row)

                if row is None:
                    try:
                        self.logic_steps.append("Row strategy {} for object {} has no activities.".format(row_strategy.__class__.__name__, obj.identifier))
                    except Exception:
                        self.logic_steps.append("Row strategy {} for object {} has no activities.".format(row_strategy.__class__.__name__, obj))
                else:
                    try:
                        self.logic_steps.append(
                            "Row strategy {} for object {} returned {} activities".format(row_strategy.__class__.__name__, obj.identifier, len(row.activities)))
                    except Exception:
                        self.logic_steps.append(
                            "Row strategy {} for object {} returned {} activities".format(
                                row_strategy.__class__.__name__, obj, len(row.activities)))


                utils.print_with_time("Info: END instantiate row for: {}".format(row_strategy.__class__.__name__))
        return [
            row for row in rows if row is not None
        ]

    def _update_learner_goals(self, active_elos):
        goal_elos = [
            elo for elo in active_elos
            if elo.ceasnconcept_term is not None and CassConfig.WELL_DEFINED_CONCEPT_TERM in elo.ceasnconcept_term
        ]

        if len(goal_elos) > 0 and set([elo.id for elo in goal_elos]) != set([goal.competency_id for goal in self.learner.goals or []]):
            new_goals = [
                Goal(context="tla-declarations.jsonld", type="Goal", competency_id=elo.id)
                for elo in goal_elos
            ]

            utils.print_with_time('INFO: Setting new goals for learner with id {} via patch request: NewGoals={}, NewPastGoals={}'.format(
                self.learner.identifier, new_goals, (self.learner.past_goals or [])+(self.learner.goals or [])
            ))

            for i in range(NUM_LEARNER_PATCH_RETRIES):
                # TODO - Competency Attempt Counters should NOT be a required field - would help avoid race conditions.
                learner_patch = Learner(name=self.learner.name, identifier=self.learner.identifier,
                                        context=self.learner.context, type=self.learner.type,
                                        competency_attempt_counters=self.learner.competency_attempt_counters,
                                        goals=new_goals,
                                        past_goals=(self.learner.past_goals or [])+(self.learner.goals or []))

                try:
                    self.query_cacher.update_learner(self.learner.identifier, self.etag, learner_patch)
                    break
                except:
                    self.learner, self.etag = self.query_cacher.get_learner(self.learner.identifier, force_update=True)

                if i == NUM_LEARNER_PATCH_RETRIES-1:
                    utils.print_with_time('WARN: Failed to update goals for learner {} after {} tries'.format(
                        self.learner.identifier, NUM_LEARNER_PATCH_RETRIES
                    ))

    def _get_learner(self, learnerId: str) -> Learner:
        return self.query_cacher.get_learner(learnerId)[0]

    def _deduplicate(self, rows: List[RecommendationRow]):
        ids = set()

        def less_than_one(recommended_activity: RecommendedActivity):
            x = recommended_activity.activity_id
            if x not in ids:
                ids.add(x)
                return False
            return True

        for row in rows:
            row.activities = list(filterfalse(less_than_one, row.activities))

    def _not_enough_content(self, active_elos, min_content_threshold):
        all_activities = filter_debug_activities(self.query_cacher.get_activities())
        all_activities = filter_pretest_activities(all_activities)
        all_activities = filter_posttest_activities(all_activities)
        max_activities_for_an_elo = 0

        for elo in active_elos:
            activities_for_elo = utils.activities_by_elo(all_activities, elo)
            max_activities_for_an_elo = max(max_activities_for_an_elo, len(activities_for_elo))

        return max_activities_for_an_elo <= min_content_threshold
