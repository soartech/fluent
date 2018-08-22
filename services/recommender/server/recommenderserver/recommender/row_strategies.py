import abc
from collections import OrderedDict
from random import randint
from typing import List, Optional

import numpy
from activity_index_client.models import LearningActivity, Organization
from cass_client import Competency
from cass_graph_client.cass_graph import CassGraph
from learner_inferences_client.models import Learner
from learner_inferences_client.models import Person
from recommenderserver.config import TokenConfig, CassConfig
from recommenderserver.models.recommendation_row import RecommendationRow
from recommenderserver.models.recommended_activity import RecommendedActivity
from recommenderserver.recommender import utils
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.tokens import Tokens
from recommenderserver.recommender.utils import MagicStrings, \
    activities_by_elo, first_time_activities, get_elo_mastery_estimate, \
    last_n_activities_attempted, elo_in_activity, \
    is_assessment, more_content_or_reference_activities


class RowStrategy(metaclass=abc.ABCMeta):
    def __init__(self, learner: Learner, query_cacher: QueryCacher, cass_graph: CassGraph, filter_locked: bool = True, filter_capstone: bool = True):
        self.learner = learner
        self.query_cacher = query_cacher
        self.cass_graph = cass_graph
        self.filter_locked = filter_locked
        self.filter_capstone = filter_capstone

    def recommendation_row(self, activities: List[LearningActivity], strategy_name, params=None) -> Optional[RecommendationRow]:
        if self.filter_locked:
            activities = self.filter_locked_activities(activities)

        if self.filter_capstone:
            activities = self.filter_capstone_activities(activities)

        if len(activities) == 0:
            return None

        activities = self.sort_activities(activities)

        return RecommendationRow(type="RecommendationRow",
                                 strategy=type(self).__name__,
                                 name=strategy_name,
                                 params=params,
                                 activities=[self.recommended_activity(activity) for activity in activities])

    def recommended_activity(self, activity: LearningActivity):
        token_decider = Tokens(self.learner, activity, self.query_cacher)
        return RecommendedActivity(activity_id=activity.identifier,
                                   tokens=token_decider.get_activity_tokens(),
                                   attempt_rate=activity.attempt_rate,
                                   popularity_rating=activity.popularity_rating,
                                   priority=self.rate_activity(activity))

    def is_activity_locked(self, activity:LearningActivity, learner: Learner):
        tlo_id = utils.get_aligned_tlo(activity)
        tlo = self.cass_graph.get_obj_by_id(tlo_id)
        tokens = self.query_cacher.get_learner_tokens(learner.identifier)
        tokens_dict = {
            token.type: token.count
            for token in tokens.tokens
        }
        if TokenConfig.TOKEN_LOGIC == TokenConfig.PossibleTokens.COMPLEX_LOGIC:

            prereqs = utils.get_prereq_tlos_and_elos(tlo, self.cass_graph)
            prereq_tokens = 0
            for prereq in prereqs:
                if prereq.id in tokens_dict:
                    prereq_tokens += tokens_dict[prereq.id]
        else:
            prereq_tokens = 0
            for token_type, token_count in tokens_dict.items():
                prereq_tokens += int(token_count)

        return prereq_tokens < tokens.unlock_threshold

    def filter_locked_activities(self, activities: List[LearningActivity]):
        return [
            activity for activity in activities
            if activity.learning_resource_type != MagicStrings.LearningResourceTypes.REAL_WORLD
               or not self.is_activity_locked(activity, self.learner)
        ]

    def filter_capstone_activities(self, activities: List[LearningActivity]):
        return [
            activity for activity in activities
            if not utils.educational_use_in_activity(activity, MagicStrings.EducationalUses.CAPSTONE) or self.__class__.__name__ == TimeForCapstone.__class__.__name__
        ]

    def filter_elos_by_mastery_probabilities(self, active_elos: List[Competency], bottom_range: float, top_range: float) -> List[Competency]:
        return_elos = []
        for elo in active_elos:
            # TODO: This needs to be sorted by most recent to least recent since there multiple mastery probabilities allowed per competency
            for mastery_probability in self.learner.mastery_probabilities:
                if utils.target_url_equals_competency(mastery_probability.competency_id, elo.id) and bottom_range <= float(mastery_probability.probability) < top_range:
                    return_elos.append(elo)
                    break
        return return_elos

    def filter_elos_by_expert_probability_estimate(self, active_elos: List[Competency]):
        return self.filter_elos_by_mastery_probabilities(active_elos, 0.8, 1.01)

    def filter_elos_by_intermediate_probability_estimate(self, active_elos: List[Competency]):
        return self.filter_elos_by_mastery_probabilities(active_elos, 0.4, 0.8)

    def filter_elos_by_novice_probability_estimate(self, active_elos: List[Competency]):
        return self.filter_elos_by_mastery_probabilities(active_elos, 0.0, 0.4)

    def filter_elos_by_mastery_estimates(self, active_elos: List[Competency], target_mastery_estimate: str):
        return_elos = []
        for elo in active_elos:
            mastery_estimate = get_elo_mastery_estimate(elo.id, self.learner)
            mastery_estimate = MagicStrings.MasteryEstimates.NOVICE if mastery_estimate is None else mastery_estimate

            if mastery_estimate == target_mastery_estimate:
                return_elos.append(elo)

        return return_elos

    def filter_elos_by_expert_mastery_estimate(self, active_elos: List[Competency]):
        return self.filter_elos_by_mastery_estimates(active_elos, MagicStrings.MasteryEstimates.EXPERT)

    def filter_elos_by_intermediate_mastery_estimate(self, active_elos: List[Competency]):
        return self.filter_elos_by_mastery_estimates(active_elos, MagicStrings.MasteryEstimates.INTERMEDIATE)

    def filter_elos_by_novice_mastery_estimate(self, active_elos: List[Competency]):
        return self.filter_elos_by_mastery_estimates(active_elos, MagicStrings.MasteryEstimates.NOVICE)

    def sort_activities(self, activities: List[LearningActivity]) -> List[LearningActivity]:
        educational_use_activities = OrderedDict({
            MagicStrings.EducationalUses.FIRST_TIME: list(),
            MagicStrings.EducationalUses.ASSESSES: list(),
            MagicStrings.EducationalUses.MORE_CONTENT: list(),
            MagicStrings.EducationalUses.REFERENCE: list(),
            MagicStrings.EducationalUses.TEAM: list(),
            "Other": list()
        })

        for activity in activities:
            for educational_use_key in educational_use_activities.keys():
                # Should only hit "other" here if no other educational uses were found.
                if (educational_use_key != "Other" and utils.educational_use_in_activity(activity, educational_use_key)) or educational_use_key == "Other":
                    educational_use_activities[educational_use_key].append(activity)
                    break

        return_activities = list()
        # Should append in the order above because of the ordered dict
        for activity_list in educational_use_activities.values():
            return_activities += activity_list

        return return_activities

    def rate_activity(self, activity) -> float:
        """
        Rate an activity that has already been matched by this strategy.
        """
        return 0.0

class ActivityRowStrategy(RowStrategy):

    @abc.abstractclassmethod
    def can_instantiate(self):
        pass

    @abc.abstractclassmethod
    def instantiate_row(self, active_elos: List[Competency], filter_obj) -> RecommendationRow:
        pass


class CompetencyRowStrategy(RowStrategy):

    @abc.abstractmethod
    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        :param active_elos: A user's active elo set.
        :return: Returns elos from the user's active elo set that can be instantiated by this row strategy.
        """
        pass

    @abc.abstractmethod
    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        """
        :param elo: The elo to instantiate this row strategy with
        :return: A RecommendationRow instantiated with the given elo.
        """
        pass


class AllActivities(ActivityRowStrategy):
    """
    This is a dummy strategy that gets all activities in the index.
    """
    def __init__(self, learner: Learner, query_cacher: QueryCacher, cass_graph: CassGraph, filter_locked: bool):
        # Override the filter_locked_activities parameter always.
        super().__init__(learner, query_cacher, cass_graph, False)

    def can_instantiate(self) -> List[bool]:
        return [True]

    def instantiate_row(self, active_elos: List[Competency], filter_obj: bool) -> RecommendationRow:
        activities = self.query_cacher.get_activities()
        return self.recommendation_row(activities, "All Activities")


class AlwaysGetFirstTenActivities(ActivityRowStrategy):
    """
    This is a dummy strategy that just gets the 10 first activities in the index.
    """
    def can_instantiate(self) -> List[bool]:
        return [True]

    def instantiate_row(self, active_elos: List[Competency], filter_obj: bool) -> RecommendationRow:
        activities = self.query_cacher.get_activities(limit=10, offset=0)
        return self.recommendation_row(activities, "Always Get First Ten Activities")


class TakeAgainActivities(ActivityRowStrategy):
    def can_instantiate(self) -> List[bool]:
        return [True]

    def instantiate_row(self, active_elos: List[Competency], filter_obj: bool) -> Optional[RecommendationRow]:
        if len(active_elos) == 0:
            return None

        elo_index = randint(0, len(active_elos)-1)
        chosen_elo = active_elos[elo_index]
        past_activities = self.learner.activity_attempt_counters
        past_activities = [self.query_cacher.get_activity(utils.mongo_id_from_url(attempt.activity_id)) for attempt in
                           past_activities]

        past_activities = [
            activity for activity in past_activities if activity is not None
        ]

        return self.recommendation_row(self.filter_activities_by_chosen_elo(chosen_elo.id, past_activities), "Take Again")

    def filter_activities_by_chosen_elo(self, chosen_elo_id:str, activities: List[LearningActivity]) -> List[LearningActivity]:
        filtered_activities = list()
        for activity in activities:
            aligned_elo_id = utils.get_aligned_elo(activity)
            if aligned_elo_id is not None and aligned_elo_id == chosen_elo_id:
                filtered_activities.append(activity)\

        return filtered_activities

class MoreFromAuthorActivities(ActivityRowStrategy):
    def can_instantiate(self) -> List[Person]:
        past_activities =  utils.last_n_activities_attempted(self.learner.activity_attempt_counters, 10, self.query_cacher)
        authors = {
            activity.author.identifier: activity.author for activity in past_activities
        }

        return list(authors.values())

    def instantiate_row(self, active_elos: List[Competency], filter_obj: Person) -> RecommendationRow:
        all_activites = self.query_cacher.get_activities()
        return self.recommendation_row(self.filter_activities_by_author(filter_obj.identifier, active_elos, all_activites), "More From Author")

    def filter_activities_by_author(self, author_id: str, active_elos: List[Competency], activities: List[LearningActivity]) -> List[LearningActivity]:
        filtered_activities = list()
        for activity in activities:
            if activity.author.identifier == author_id:
                aligned_elo_id = utils.get_aligned_elo(activity)
                if aligned_elo_id is not None and aligned_elo_id in [elo.id for elo in active_elos]:
                    filtered_activities.append(activity)
        return filtered_activities

    def rate_activity(self, activity):
        return 2.5


class MoreFromProviderActivities(ActivityRowStrategy):
    def can_instantiate(self) -> List[Organization]:
        past_activities =  utils.last_n_activities_attempted(self.learner.activity_attempt_counters, 10, self.query_cacher)

        providers = {
            activity.provider.identifier: activity.provider for activity in past_activities
        }
        return list(providers.values())

    def instantiate_row(self, active_elos: List[Competency], filter_obj: Organization) -> RecommendationRow:
        all_activities = self.query_cacher.get_activities()
        return self.recommendation_row(self.filter_activities_by_provider(filter_obj.identifier, active_elos, all_activities), "More From Provider")

    def filter_activities_by_provider(self, organization_id: str, active_elos: List[Competency], activities: List[LearningActivity]) -> List[LearningActivity]:
        filtered_activities = list()
        for activity in activities:
            if activity.provider.identifier == organization_id:
                aligned_elo_id = utils.get_aligned_elo(activity)
                if aligned_elo_id is not None and aligned_elo_id in [elo.id for elo in active_elos]:
                    filtered_activities.append(activity)

        return filtered_activities

    def rate_activity(self, activity):
        return 2.5


class MoreVideosActivities(ActivityRowStrategy):
    def can_instantiate(self) -> List[str]:
        return [utils.MagicStrings.LearningResourceTypes.VIDEO]

    def instantiate_row(self, active_elos: List[Competency], filter_obj: str) -> RecommendationRow:
        all_activities = self.query_cacher.get_activities()
        return self.recommendation_row(self.filter_activites_by_activity_type(filter_obj, active_elos, all_activities), "More Videos")

    def filter_activites_by_activity_type(self, activity_type: str, active_elos: List[Competency], activities: List[LearningActivity]) -> List[LearningActivity]:
        filtered_activities = list()
        for activity in activities:
            if activity.learning_resource_type == activity_type:
                aligned_elo_id = utils.get_aligned_elo(activity)
                if aligned_elo_id is not None and aligned_elo_id in [elo.id for elo in active_elos]:
                    filtered_activities.append(activity)
        return filtered_activities

    def rate_activity(self, activity):
        return 2.5


class ReviewActivities(CompetencyRowStrategy):
    """
    This strategy returns activities for ELOs where the Instructional Type is 'More Content'
    (meaning it's review material). The instantiation rule can be used as is for the well-defined case as well.
    """

    def __init__(self, learner: Learner, query_cacher: QueryCacher, cass_graph: CassGraph, filter_locked: bool):
        super().__init__(learner, query_cacher, cass_graph, filter_locked)

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        Instantiate up to 3 rows for each ELO where the mastery is 'forgotten'. Start from most recently forgot.
        :return:
        """
        forgotten_competencies = [
            estimate.competency_id for estimate in self.learner.mastery_estimates
            if estimate.mastery == MagicStrings.MasteryEstimates.FORGOT
        ]

        forgotten_elos = [
            self.cass_graph.get_obj_by_id(comp_id) for comp_id in forgotten_competencies
            if self.cass_graph.get_obj_by_id(comp_id) is not None
                and self.cass_graph.get_obj_by_id(comp_id).dctermstype == MagicStrings.DC_TERM_TYPES.ELO
        ]

        return forgotten_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        return self.recommendation_row(activities=elo_activities, strategy_name="Review")



class AffectBored(CompetencyRowStrategy):
    """
    This row selects activities for an ELO where the Interactivity Level is 'active' or 'mixed' and the
    Challenge Level is 'moderate' or 'complex'.
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        If user is 'bored', instantiate one row for the user's active ELO in the well-defined ELO sequence.
        :return:
        """
        if self.learner.bored:
            return active_elos
        else:
            return []

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if (activity.interactivity_type == utils.MagicStrings.InteractivityTypes.COMPLEX_PARTICIPATION
                    or activity.interactivity_type == utils.MagicStrings.InteractivityTypes.LIMITED_PARTICIPATION)
               and (utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.MODERATE)
                    or utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.COMPLEX))
        ]

        return self.recommendation_row(activities=elo_activities, strategy_name="Challenging and Interactive")

    def rate_activity(self, activity):
        return 4.0


class AffectFrustratedOrBored(CompetencyRowStrategy):
    """
    This row selects activities for an ELO where the  Interactivity Level is 'active' or 'mixed' and the
    Challenge Level is 'simple'
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        If user is 'frustrated' or the user is 'bored', instantiate one row for the user's active ELO in the
        well-defined ELO sequence.
        :return:
        """
        if self.learner.frustrated or self.learner.bored:
            return active_elos
        else:
            return []

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if (activity.interactivity_type == utils.MagicStrings.InteractivityTypes.COMPLEX_PARTICIPATION
                    or activity.interactivity_type == utils.MagicStrings.InteractivityTypes.LIMITED_PARTICIPATION)
               and utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.SIMPLE)
        ]

        return self.recommendation_row(activities=elo_activities, strategy_name="Approachable and Interactive")

    def rate_activity(self, activity):
        return 4.0


class AffectConfusedOrNew(CompetencyRowStrategy):
    """
    This row selects activities for an ELO where the Interactivity Level is 'passive' and the Challenge Level is 'Simple'
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        If user is 'confused' or new to the ELO (ELO is active but no activity history for it),
        instantiate one row for the user's active ELO in the well-defined ELO sequence.
        :return:
        """
        if self.learner.confused:
            return active_elos
        return [elo for elo in active_elos if self._no_activity_history(elo.id)]

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if activity.interactivity_type == utils.MagicStrings.InteractivityTypes.PASSIVE
               and utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.SIMPLE)
        ]
        return self.recommendation_row(activities=elo_activities, strategy_name="Essential Activities")

    def _no_activity_history(self, elo_id: str) -> bool:
        for attempt in self.learner.activity_attempt_counters:
            activity_id = attempt.activity_id
            if int(attempt.attempts) > 0:
                activity = self.query_cacher.get_activity(activity_id)
                if utils.elo_in_activity(elo_id, activity):
                    return False
        return True

    def rate_activity(self, activity):
        return 4.0


class PopularActivities(CompetencyRowStrategy):
    """
    This row selects activities for an ELO that are the most popular.
    """

    def rate_activity(self, activity: LearningActivity) -> float:
        return 0.0 if activity.attempt_rate is None else float(activity.attempt_rate)

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        Always instantiate one
        :return:
        """
        return active_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if activity.attempt_rate is not None
        ]
        elo_activities = sorted(elo_activities, key=lambda activity: activity.attempt_rate, reverse=True)
        return self.recommendation_row(activities=elo_activities, strategy_name="Popular Activities")


class HighestRatedActivities(CompetencyRowStrategy):
    """
    This row selects activities for an ELO that are the highest rated.
    """

    def rate_activity(self, activity) -> float:
        return 0.0 if activity.popularity_rating is None else activity.popularity_rating

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        Always instantiate one
        :return:
        """
        return active_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities if activity.popularity_rating is not None
        ]

        elo_activities = sorted(elo_activities, key=lambda activity: activity.popularity_rating, reverse=True)
        return self.recommendation_row(activities=elo_activities, strategy_name="Highest Rated Activities")


class ChallengingActivities(CompetencyRowStrategy):
    """
    This row selects activities for an ELO where the Challenge Level is 'Complex'
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        If the user has Mastery Probability x >= .8 then instantiate one row for the user's active ELO in the
        well-defined ELO sequence.
        :return:
        """
        return self.filter_elos_by_expert_probability_estimate(active_elos)

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.COMPLEX)
        ]
        return self.recommendation_row(activities=elo_activities, strategy_name="Challenging Activities")

    def rate_activity(self, activity):
        return 4.0


class IntermediateActivities(CompetencyRowStrategy):
    """
    This row selects activities for an ELO where the Challenge Level is 'Moderate'
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        If the user has Mastery Probability .4 >= x > .8 then instantiate one row for the user's active ELO in the
        well-defined ELO sequence.
        :return:
        """
        return self.filter_elos_by_intermediate_probability_estimate(active_elos)

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.MODERATE)
        ]
        return self.recommendation_row(activities=elo_activities, strategy_name="Intermediate Activities")


class IntroductoryActivities(CompetencyRowStrategy):
    """
    This row selects activities for an ELO where the Challenge Level is 'Simple'
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        """
        If the user has Mastery Probability 0 > x > .4 then instantiate one row for the user's active ELO in the
        well-defined ELO sequence.
        :return:
        """
        return self.filter_elos_by_novice_probability_estimate(active_elos)

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [
            activity for activity in elo_activities
            if utils.has_challenge_level(elo.id, activity, utils.MagicStrings.ChallengeLevels.SIMPLE)
        ]
        return self.recommendation_row(activities=elo_activities, strategy_name="Introductory")


class NewCompetency(CompetencyRowStrategy):
    """
    This row selects random activities for an ELO for which the user has no activity history.
    It is applicable only to ill-defined ELOs
    """
    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        applicable_elos = [elo for elo in active_elos if CassConfig.ILL_DEFINED_CONCEPT_TERM in elo.ceasnconcept_term]

        competency_history = [competency_attempt_counter.competency_id for competency_attempt_counter in
                              self.learner.competency_attempt_counters]

        return [elo for elo in applicable_elos if elo.id not in competency_history]

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        if len(elo_activities) <= 10:
            return self.recommendation_row(activities=elo_activities, strategy_name="New Competency")

        return self.recommendation_row(activities=numpy.random.choice(elo_activities, 10, replace=False), strategy_name="New Competency")


class AllActivitiesForCompetency(CompetencyRowStrategy):
    """
    This is a debugging strategy that returns all activities for a given ELO.
    """
    def can_instantiate(self, competency: List[Competency]):
        return competency

    def instantiate_row(self, competency: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        return self.recommendation_row(activities=elo_activities,
                                       strategy_name="All activities for {}".format(competency.name),
                                       params={"competency": competency.name})


class Shiny(CompetencyRowStrategy):
    """
    This strategy picks shiny activities for an ELO.
    A Shiny Level of Shiny indicates an activity that is attractive or rewarding
    to the learners and it will be used to space out the rewards if there are any.
    """

    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        return active_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        activities = [activity for activity in self.query_cacher.get_activities() if utils.is_shiny(activity)]
        return self.recommendation_row(activities=activities, strategy_name="Shiny Activities")


class MoveToNextSection(CompetencyRowStrategy):
    """
    This strategy shows all formative assessments for the active ELO.
    """

    def __init__(self, learner: Learner, query_cacher: QueryCacher, cass_graph: CassGraph,
                 filter_locked: bool):
        super().__init__(learner, query_cacher, cass_graph, filter_locked)
        self.filter_assessments = False

    def can_instantiate(self, active_elos: List[Competency]):
        return active_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = [activity for activity in elo_activities if is_assessment(activity)]

        return self.recommendation_row(
            activities=elo_activities,
            strategy_name="Move to Next Section: Assessments for {}".format(elo.name))


class MoreFromPreviousTLOs(ActivityRowStrategy):
    """
    This strategy shows activities from the all previously mastered ELOs
    that have either not been taken or are metacognitive prompts
    """

    def can_instantiate(self) -> List[bool]:
        return [True]

    def instantiate_row(self, active_elos: List[Competency], filter_obj) -> RecommendationRow:
        recommended_activities = []
        activity_attempt_ids = []
        for elo in active_elos:
            prev_elos = self.get_prev_elos(elo)
            activities = self.query_cacher.get_activities()
            for prev_elo in prev_elos:
                elo_activities = activities_by_elo(activities, prev_elo)

                for attempt in self.learner.activity_attempt_counters:
                    activity_attempt_ids.append(attempt.activity_id)

                for activity in elo_activities:
                    if activity.learning_resource_type == MagicStrings.LearningResourceTypes.METACOGNITIVE_PROMPT:
                        recommended_activities.append(activity)
                        continue
                    if activity.identifier not in activity_attempt_ids:
                        recommended_activities.append(activity)

        # Given elo_activities, only pass the activities that have either not been taken or are metacognitive prompts
        return self.recommendation_row(activities=recommended_activities, strategy_name="More from Previous TLOs")

    def get_prev_elos(self, active_elo: Competency) -> List[Competency]:
        elo = self.cass_graph.get_obj_by_id(active_elo.id)
        parent_tlo = self.cass_graph.get_parent_top_level_competency(elo)
        prev_tlo = self.cass_graph.get_previous_neighbor(parent_tlo)
        return_elos = list()  # type: List[Competency]
        while prev_tlo is not None:
            children = self.cass_graph.get_children_ordered(prev_tlo)
            if children is not None:
                for child_elo in children:
                    child_children = self.cass_graph.get_children_ordered(child_elo)
                    if child_children is not None:
                        return_elos += child_children
                    else:
                        return_elos.append(child_elo)
            prev_tlo = self.cass_graph.get_previous_neighbor(prev_tlo)

        return return_elos  # Question: will this get a neighbor who doesn't have the same parent?
        # Most likely answer: no; it looks like "get_ELO_chain" wouldn't work if that was the case


class FirstTimeNotAppropriateForExperts(CompetencyRowStrategy):
    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        return self.filter_elos_by_expert_mastery_estimate(active_elos)

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = first_time_activities(elo_activities)
        return self.recommendation_row(elo_activities, "Content Not At The Right Level")

    def rate_activity(self, activity):
        return -10.0


class MoreContentOrReferenceNotAppropriateForNovices(CompetencyRowStrategy):
    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        return self.filter_elos_by_novice_mastery_estimate(active_elos)

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        elo_activities = more_content_or_reference_activities(elo_activities)
        return self.recommendation_row(elo_activities, "Content Not At The Right Level")

    def rate_activity(self, activity):
        return -25.0


class NewActivities(CompetencyRowStrategy):
    def can_instantiate(self, active_elos: List[Competency]) -> List[Competency]:
        return active_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        activity_history = [activity_attempt_counter.activity_id for activity_attempt_counter in
                            self.learner.activity_attempt_counters]
        new_activities = [activity for activity in elo_activities if activity.identifier not in activity_history]

        return self.recommendation_row(new_activities, "New Activity")

    def rate_activity(self, activity):
        return 5.0


class TimeForCapstone(CompetencyRowStrategy):
    def can_instantiate(self, active_elos: List[Competency]):
        mastered_badge_competencies = []
        for elo in active_elos:
            parent = self.cass_graph.get_parent_competency(elo)
            if parent is None:
                mastery_estimate = get_elo_mastery_estimate(elo.id, self.learner)
                if mastery_estimate is not None and mastery_estimate == MagicStrings.MasteryEstimates.EXPERT:
                    mastered_badge_competencies.append(elo)

        return mastered_badge_competencies

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]):
        capstone_activities = list()
        for activity in elo_activities:
            if "Capstone" in activity.educational_use:
                capstone_activities.append(activity)

        return self.recommendation_row(capstone_activities, "Time for a Capstone Assessment")

    def rate_activity(self, activity):
        return 30.0


class TimeForAnAssessment(CompetencyRowStrategy):
    """
    If the user has performed taken n activities in a row for the same competency that were not assessments,
    then prioritize assessments for that competency.
    """
    NUM_BEFORE_ASSESSMENT = 3
    HISTORY_LIMIT = 20

    def can_instantiate(self, active_elos: List[Competency]):
        elo_id_to_attempted_activities = {elo.id: [] for elo in active_elos}

        # Only look at last n activities from learner (list is [most recent, 2nd most recent, ... nth most recent])
        last_activities_attempted = last_n_activities_attempted(self.learner.activity_attempt_counters,
                                                                self.HISTORY_LIMIT, self.query_cacher)

        return_elos = []
        for elo in active_elos:
            for activity in last_activities_attempted:
                if elo_in_activity(elo.id, activity):
                    if is_assessment(activity):
                        break

                    elo_id_to_attempted_activities[elo.id].append(activity)
                    if len(elo_id_to_attempted_activities[elo.id]) == self.NUM_BEFORE_ASSESSMENT:
                        return_elos.append(elo)
                        break

        return return_elos

    def instantiate_row(self, elo: Competency, elo_activities: List[LearningActivity]) -> RecommendationRow:
        assessments_for_elo = [activity for activity in elo_activities if is_assessment(activity)]
        return self.recommendation_row(assessments_for_elo, "Time for an Assessment")

    def rate_activity(self, activity):
        return 10.0
