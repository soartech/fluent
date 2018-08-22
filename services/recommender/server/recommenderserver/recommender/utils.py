import heapq
import pickle
from datetime import datetime, timezone
from typing import List, Optional

import pkg_resources
from activity_index_client import LearningActivity
from cass_client.models import Competency
from cass_graph_client.cass_graph import CassGraph
from learner_inferences_client import ActivityAttemptCounter, Learner, MasteryProbability
from learner_inferences_server.amqp_listener import inference_utils
from recommenderserver.config import CassConfig
from recommenderserver.recommender.query_cacher import QueryCacher
import uuid
from math import ceil

RECOGNIZE_GOALS = True

def mongo_id_from_url(url: str) -> Optional[str]:
    """
    :param url: A url where the mongo id is the last element.
    :return: the mongo id
    """
    try:
        last_part = url.split('/')[-1]
        return last_part
    except Exception as e:
        return None


def get_last_activity_url_identifier(learner: Learner) -> Optional[str]:
    last_activity_attempt_counter = get_last_activity_attempt_counter(learner.activity_attempt_counters)
    if last_activity_attempt_counter is not None:
        return last_activity_attempt_counter.activity_id
    else:
        return None


def get_last_activity_attempt_counter(
        activity_attempt_counters: List[ActivityAttemptCounter]) -> Optional[ActivityAttemptCounter]:
    if activity_attempt_counters is None or len(activity_attempt_counters) == 0:
        return None

    return max(activity_attempt_counters,
               key=lambda x: x.last_attempt_date_time.replace(tzinfo=timezone.utc))


def get_check_on_learning_assessment_acitivity_id(activity: LearningActivity) -> Optional[str]:
    # TODO: I think their should be 0-N appropriate-assessment-alignment objects per activity, but we're just returning first for now
    # TODO: I'm not sure if the additional_type should be the url below or simply 'AppropriateAssessmentAlignment'

    for alignment in activity.educational_alignment:
        if alignment.additional_type == MagicStrings.AdditionalTypes.APPROPRIATE_ASSESSMENT_ALIGNMENT:
            return alignment.target_url
    return None


def elo_in_activity(elo: str, activity: LearningActivity) -> bool:
    # TODO - fix this elsewhere (probably)
    if activity is None:
        return False

    for alignment in activity.educational_alignment:
        if target_url_equals_competency(alignment.target_url, elo) and alignment.additional_type == MagicStrings.AdditionalTypes.ELO_ALIGNMENT:
            return True

    return False

def activities_by_elo(activities, elo):
    return [activity for activity in activities if elo_in_activity(elo.id, activity)]

def activities_by_elo_id(activities, elo_id):
    return [activity for activity in activities if elo_in_activity(elo_id, activity)]

def get_aligned_elo(activity: LearningActivity) -> Optional[str]:
    for alignment in activity.educational_alignment:
        if alignment.additional_type == MagicStrings.AdditionalTypes.ELO_ALIGNMENT:
            return alignment.target_url

    return None


def get_aligned_tlo(activity: LearningActivity) -> Optional[str]:
    for alignment in activity.educational_alignment:
        if alignment.additional_type == MagicStrings.AdditionalTypes.TLO_ALIGNMENT:
            return alignment.target_url

    return None


def get_prereq_tlos_and_elos(tlo: Competency, cass_graph: CassGraph) -> List[Competency]:
    prereqs = list()
    prev_tlo = cass_graph.get_first_top_level_competency()
    while prev_tlo.id not in tlo.id and tlo.id not in prev_tlo.id:
        prereqs.append(prev_tlo)
        prereqs += cass_graph.get_competency_chain(prev_tlo)
        prev_tlo = cass_graph.get_next_neighbor(prev_tlo)
    return prereqs


def get_elo_mastery_estimate(elo_id: str, learner: Learner) -> Optional[str]:
    for me in learner.mastery_estimates:
        if target_url_equals_competency(me.competency_id, elo_id):
            return me.mastery

    return None


def is_shiny(activity: LearningActivity) -> bool:
    for alignment in activity.educational_alignment:
        if alignment.additional_type == MagicStrings.AdditionalTypes.SHINY_ALIGNMENT \
                and alignment.alignment_type == MagicStrings.AlignmentTypes.SHINY:
            return True
    return False


def tlo_in_activity(tlo: str, activity: LearningActivity) -> bool:
    for alignment in activity.educational_alignment:
        if target_url_equals_competency(alignment.target_url, tlo) and alignment.additional_type == MagicStrings.AdditionalTypes.TLO_ALIGNMENT:
            return True

    return False


def assessment_activities_for_elo(activities: List[LearningActivity], elo: Competency):
    return [activity for activity in activities if is_assessment_for_elo(activity, elo)]


def is_assessment_for_elo(activity: LearningActivity, competency: Competency):
    for alignment in activity.educational_alignment:
        if alignment.alignment_type == MagicStrings.AlignmentTypes.ASSESSES and target_url_equals_competency(
                alignment.target_url, competency.id):
            return True
    return False


def get_current_elos(learner: Learner, cass_graph: CassGraph) -> List[Competency]:
    if RECOGNIZE_GOALS:
        current_elos = get_current_elos_goals(learner, cass_graph)
        if len(current_elos) > 0:
            return current_elos
        else:
            return get_current_elos_push(learner, cass_graph)
    else:
        return get_current_elos_push(learner, cass_graph)


def get_current_elos_goals(learner: Learner, cass_graph: CassGraph) -> List[Competency]:
    tlo = cass_graph.get_first_top_level_competency()

    while tlo is not None:
        elos = cass_graph.get_competency_chain(tlo)
        # Well defined TLO
        if CassConfig.WELL_DEFINED_CONCEPT_TERM in tlo.ceasnconcept_term:
            # Need to walk down the chain for the well-defined case.
            for elo in elos:
                elo_children = cass_graph.get_children_ordered(elo)
                # If the ELO has children, check the children for an ELO mastery estimate that is not 'held' or 'forgotten'
                if elo_children is not None and len(elo_children) > 0:
                    for child in elo_children:
                        mastery_estimate = get_elo_mastery_estimate(child.id, learner)
                        if mastery_estimate is not None:
                            if mastery_estimate != MagicStrings.MasteryEstimates.HELD and mastery_estimate != MagicStrings.MasteryEstimates.FORGOT:
                                return [child]
                        else:
                            return [child]

                # Regardless of if it has children, we also want to check the ELO itself is 'held', because it also can have content
                mastery_estimate = get_elo_mastery_estimate(elo.id, learner)
                if mastery_estimate is not None:
                    if mastery_estimate != MagicStrings.MasteryEstimates.HELD and mastery_estimate != MagicStrings.MasteryEstimates.FORGOT:
                        return [elo]
                else:
                    # If we did not find any mastery estimate for that ELO, that is our current ELO.
                    return [elo]

        # Ill-defined TLO - use learner goals
        else:
            current_elos = list()
            learner_goal_competency_ids = [
                goal.competency_id for goal in learner.goals
            ]

            for goal_comp_id in learner_goal_competency_ids:
                elo_obj = cass_graph.competency_objs.get(goal_comp_id, None)
                if elo_obj is not None:
                    elo_children = cass_graph.get_children_ordered(elo_obj)
                    incomplete_child_elo_found = False
                    if elo_children is not None and len(elo_children) > 0:
                        for child in elo_children:
                            mastery_estimate = get_elo_mastery_estimate(child.id, learner)
                            if mastery_estimate is not None:
                                if mastery_estimate != MagicStrings.MasteryEstimates.HELD and mastery_estimate != MagicStrings.MasteryEstimates.FORGOT:
                                    current_elos.append(child)
                                    incomplete_child_elo_found = True
                                    break
                            else:
                                # If we did not find any mastery estimate for that child ELO, that is one of the current ELOs.
                                current_elos.append(child)
                                incomplete_child_elo_found = True
                                break
                    # Regardless of if it has children, if we did not find a child that is incomplete, we also want to check if the ELO itself is 'held' or 'forgotten'
                    if not incomplete_child_elo_found:
                        mastery_estimate = get_elo_mastery_estimate(elo.id, learner)
                        if mastery_estimate is not None:
                            if mastery_estimate != MagicStrings.MasteryEstimates.HELD and mastery_estimate != MagicStrings.MasteryEstimates.FORGOT:
                                current_elos.append(elo)
                        else:
                            # If we did not find any mastery estimate for that ELO, that is one of the current ELOs.
                            current_elos.append(elo)

            # Will return an empty list if the current goals' sub-ELOs are all mastered.
            return current_elos

        tlo = cass_graph.get_next_neighbor(tlo)

    return []

def get_current_elos_push(learner: Learner, cass_graph: CassGraph) -> List[Competency]:
    tlo = cass_graph.get_first_top_level_competency()

    while tlo is not None:
        elos = cass_graph.get_competency_chain(tlo)
        # Need to walk down the chain
        for elo in elos:
            elo_children = cass_graph.get_children_ordered(elo)
            if elo_children is not None and len(elo_children) > 0:
                for child in elo_children:
                    mastery_estimate = get_elo_mastery_estimate(child.id, learner)
                    if mastery_estimate is not None:
                        if mastery_estimate != MagicStrings.MasteryEstimates.HELD and mastery_estimate != MagicStrings.MasteryEstimates.FORGOT:
                            return [child]
                    else:
                        # If we did not find any mastery estimate for that child ELO, that is one of the current ELOs.
                        return [child]

            # Do this regardless of children
            mastery_estimate = get_elo_mastery_estimate(elo.id, learner)
            if mastery_estimate is not None:
                if mastery_estimate != MagicStrings.MasteryEstimates.HELD and mastery_estimate != MagicStrings.MasteryEstimates.FORGOT:
                    return [elo]
            else:
                # If we did not find any mastery estimate for that ELO, that is one of the current ELOs.
                return [elo]

        tlo = cass_graph.get_next_neighbor(tlo)

    return []


def has_challenge_level(elo_id: str, activity: LearningActivity, challenge_level: str):
    for alignment in activity.educational_alignment:
        if alignment.additional_type == MagicStrings.AdditionalTypes.CHALLENGE_LEVEL_ALIGNMENT and target_url_equals_competency(alignment.target_url, elo_id) and alignment.alignment_type == challenge_level:
            return True
    return False


def has_learner_seen_activity(learner: Learner, activity:LearningActivity) -> bool:
    for attempt in learner.activity_attempt_counters:
        activity_id = attempt.activity_id
        if activity_id == activity.identifier and int(attempt.attempts) > 0:
            return True
    return False


class MagicStrings(object):
    class AdditionalTypes:
        APPROPRIATE_ASSESSMENT_ALIGNMENT = 'AppropriateAssessmentAlignment'
        JOB_TASK_ALIGNMENT = 'https://tla.adl.net/alignment-types/job-task'
        KSA_ALIGNMENT = 'https://tla.adl.net/alignment-types/ksa'
        TLO_ALIGNMENT = 'TLOAlignment'
        ELO_ALIGNMENT = 'ELOAlignment'
        CHALLENGE_LEVEL_ALIGNMENT = 'ChallengeLevelAlignment'
        SHINY_ALIGNMENT = 'ShinyAlignment'
        EXPECTED_TLO_MASTERY_ALIGNMENT = 'https://tla.adl.net/alignment-types/expected-tlo-mastery'
        EXPECTED_ELO_MASTERY_ALIGNMENT = 'https://tla.adl.net/alignment-types/expected-elo-mastery'

    class UnitTestAssertions:
        SELF_REPORT_URL_IDENTIFIER = "https://activity-index-service/activities/5b01c5c92a78f29959236bd4"
        UNIT_ASSESSMENT_IDENTIFIER = "https://activity-index-service/activities/5b01c5c92a78f29959236bd5"

    class LearningResourceTypes:
        TEXT = "Text"""
        IMAGE = "Image"
        VIDEO = "Video"
        AUDIO = "Audio"
        SLIDEWHO = "Slideshow"
        LEARNING_CHECK_ASSESSMENT = "LearningCheckAssessment"
        FORMATIVE_ASSESSMENT = "FormativeAssessment"
        UNIT_ASSESSMENT = "UnitAssessment"
        GAME = "Game"
        SIMULATION = "Simulation"
        VIRTUAL_REALITY = "VirtualReality"
        AUGMENTED_REALITY = "AugmentedReality"
        REAL_WORLD = "RealWorld"
        HELP_DOC = "HelpDoc"
        WAKEUP = "Wakeup"
        METACOGNITIVE_PROMPT = "MetacognitivePrompt"

        @classmethod
        def get_assessment_types(cls):
            return [cls.LEARNING_CHECK_ASSESSMENT, cls.FORMATIVE_ASSESSMENT, cls.UNIT_ASSESSMENT]

    class AlignmentTypes:
        SHINY = 'Shiny'
        TEACHES_FIRST_TIME = "TeachesFirstTime"
        TEACHES_REVIEW = "TeachesReview"
        REFERENCE = "Reference"
        ASSESSES = "Assesses"

    class ChallengeLevels:
        SIMPLE = "Simple"
        COMPLEX = "Complex"
        EASY = "Easy"
        MODERATE = "Moderate"

    class InteractivityTypes:
        LIMITED_PARTICIPATION = "LimitedParticipation"
        COMPLEX_PARTICIPATION = "ComplexParticipation"
        PASSIVE = "Passive"

    class EducationalUses:
        MORE_CONTENT = "MoreContent"
        ASSESSES = "Assesses"
        REFERENCE = "Reference"
        SELF_REPORT = "SelfReport"
        FIRST_TIME = "FirstTime"
        PRE_TEST = "PreTest"
        POST_TEST = "PostTest"
        DEBUG = "Debug"
        TEAM = "Team"
        PLACEHOLDER = "Placeholder"
        OLD = "Old"
        CAPSTONE = "Capstone"

    class MasteryEstimates:
        NOT_HELD = "not held"
        HELD = "held"
        FORGOT = "forgotten"
        UNKNOWN = "unknown"
        NOVICE = "novice"
        INTERMEDIATE = "intermediate"
        EXPERT = "expert"


    class DC_TERM_TYPES:
        ELO = "ELO"


def last_activity_attempts(activity_attempt_counters: List[ActivityAttemptCounter], last_n: int) -> List[
    ActivityAttemptCounter]:
    if activity_attempt_counters is None:
        return []
    return heapq.nlargest(last_n, activity_attempt_counters, key=lambda x: x.last_attempt_date_time.replace(tzinfo=timezone.utc))


def last_n_activities_attempted(activity_attempt_counters: List[ActivityAttemptCounter], last_n: int,
                                query_cacher: QueryCacher) -> List[LearningActivity]:
    activity_attempts = last_activity_attempts(activity_attempt_counters, last_n)
    last_n_activities = [query_cacher.get_activity(mongo_id_from_url(attempt.activity_id)) for attempt in
                         activity_attempts]
    return [
        activity for activity in last_n_activities if activity is not None
    ]


def load_or_instantiate(package_name, klass, *args):
    resource_name = str(klass.__name__) + '_' + '_'.join(str(arg) for arg in args) + '.pkl'
    if pkg_resources.resource_exists(package_name, resource_name):
        return pickle.load(pkg_resources.resource_stream(package_name, resource_name))
    return klass(*args)


def target_url_equals_competency(target_url: Optional[str], comp_id: Optional[str]):
    if target_url is None or comp_id is None:
        return False
    try:
        target_url = inference_utils.sanitize_competency_id(target_url)
    except ValueError:
        target_url = target_url.replace("http://", "https://")
    try:
        comp_id = inference_utils.sanitize_competency_id(comp_id)
    except ValueError:
        comp_id = comp_id.replace("http://", "https://")
    return target_url == comp_id


def is_assessment(activity: LearningActivity):
    for alignment in activity.educational_alignment:
        if alignment.alignment_type == MagicStrings.AlignmentTypes.ASSESSES:
            return True
        return False


def filter_assessment_activities(activities):
    return [
        activity for activity in activities if not is_assessment(activity)
    ]

def educational_use_in_activity(activity: LearningActivity, educational_use: str) -> bool:
    return educational_use in activity.educational_use

if __name__ == '__main__':
    print(load_or_instantiate('recommenderserver.resources', CassGraph, '59e884bb-510b-4f36-8443-8c3842336e28'))


def filter_debug_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    # Only return activities that are not debug activities
    return [
        activity for activity in activities
        if not educational_use_in_activity(activity, MagicStrings.EducationalUses.DEBUG)
    ]

def filter_old_activities(activities):
    # Only return activities that are not old activities
    return [
        activity for activity in activities
        if not educational_use_in_activity(activity, MagicStrings.EducationalUses.OLD)
    ]

def filter_pretest_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    return [
        activity for activity in activities
        if not educational_use_in_activity(activity, MagicStrings.EducationalUses.PRE_TEST)
    ]

def filter_posttest_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    return [
        activity for activity in activities
        if not educational_use_in_activity(activity, MagicStrings.EducationalUses.POST_TEST)
    ]

def filter_placeholder_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    return [
        activity for activity in activities
        if not educational_use_in_activity(activity, MagicStrings.EducationalUses.PLACEHOLDER)
    ]

def first_time_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    return [
        activity for activity in activities
        if educational_use_in_activity(activity, MagicStrings.EducationalUses.FIRST_TIME)
    ]

def more_content_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    return [
        activity for activity in activities
        if educational_use_in_activity(activity, MagicStrings.EducationalUses.MORE_CONTENT)
    ]

def more_content_or_reference_activities(activities: List[LearningActivity]) -> List[LearningActivity]:
    return [
        activity for activity in activities
        if
        educational_use_in_activity(activity, MagicStrings.EducationalUses.MORE_CONTENT) or educational_use_in_activity(
            activity, MagicStrings.EducationalUses.REFERENCE)
    ]

def get_goals_and_subgoals(learner: Learner, cass_graph: CassGraph) -> List[Competency]:
    goals_and_subgoals = list()
    learner_goal_competencies = [cass_graph.get_obj_by_id(goal.competency_id) for goal in learner.goals]
    goals_and_subgoals.extend(learner_goal_competencies)
    for goal_competency in learner_goal_competencies:
        goals_and_subgoals.extend(cass_graph.get_descendants(goal_competency))
    return goals_and_subgoals

def get_goals_and_subgoals_using_prequisites(learner: Learner, cass_graph: CassGraph, return_all=True) -> List[Competency]:
    """
    Traverses up and down the graph using prerequisites and mastery estimates to determine the available,
    unblocked, unmastered competencies to work on, either as subgoals of the learner's goal, or as prerequisties
    to the learners goal if that goal has unmastered prerequisites
    """
    goals_and_subgoals = list()
    mastery_ids = [estimate.competency_id for estimate in learner.mastery_estimates if estimate.mastery == MagicStrings.MasteryEstimates.EXPERT]

    learner_goal_competencies = []
    for goal in learner.goals:
        competency = cass_graph.get_obj_by_id(goal.competency_id)
        if competency is not None:
            learner_goal_competencies.append(competency)
        else:
            print('Unable to find learner goal "{}" in framework'.format(goal.competency_id))

    for competency in learner_goal_competencies:
        if cass_graph.prerequisites_met(competency, mastery_ids):
            if cass_graph.is_leaf(competency):
                goals_and_subgoals.append(competency)
            else:
                if not cass_graph.is_mastered(competency, mastery_ids):
                    goals_and_subgoals.append(competency)
                goals_and_subgoals.extend(cass_graph.get_unblocked_unmastered_descendants(competency, mastery_ids, only_leaves=False))
        else:
            goals_and_subgoals.extend(cass_graph.get_unblocked_unmastered_ancestors(competency, mastery_ids, only_leaves=False))

    #if we only have leaf nodes in goals_and_subgoals, then return the full list now.

    if are_all_leaf_nodes(competencies=goals_and_subgoals, cass_graph=cass_graph):
        return goals_and_subgoals

    #IF we were told to GET MORE (learner UI button) then just return the full list now.
    if return_all:
        return goals_and_subgoals

    #the point of the following is to pick fewer ELOs because goals_and_subgoals is sometimes too large.
    #if we are here then we have at least one node that is a direct parent of leaf nodes. assume these are novice, intermediate, expert nodes
    #  find the novice, intermediate, and expert nodes in goals_and_subgoals
    leaf_parents = find_leaf_parents(goals_and_subgoals, cass_graph)

    # If for some reason we didn't find any leaf parents, return out here.
    if len(leaf_parents) == 0:
        return goals_and_subgoals

    #  next, only consider the lowest level of the nodes found - e.g. remove intermediate nodes if any novice nodes are in the list, etc.
    leaf_parents = get_lowest_leaf_parents(leaf_parents, cass_graph)

    #  out of the remaining novice/inter/expert nodes, pick the one with HIGHEST recent mastery probability.
    target_leaf_parent = get_target_leaf_parent_by_mastery_prob(leaf_parents, learner)

    #after we pick one ELO to return, also include all its ancestors and children that are in the goals_and_subgoals.

    goals_and_subgoals = get_new_subgoals(goals_and_subgoals, target_leaf_parent, cass_graph)

    print_with_time("Recommending with subgoals: {}".format([goal.ceasncoded_notation for goal in goals_and_subgoals]))
    return goals_and_subgoals


def are_all_leaf_nodes(competencies: List[Competency], cass_graph: CassGraph):
    for competency in competencies:
        if not cass_graph.is_leaf(competency):
            return False

    return True


def print_with_time(msg):
    if msg is not None and len(msg) > 0:
        time = datetime.utcnow().replace(tzinfo=timezone.utc)
        print("[{}] - {}".format(str(time), msg), flush=True)


def print_with_time_split(msg, tag="Info"):
    character_limit = 5000
    if msg is not None and len(msg) > 0:
        part_num = int(ceil(len(msg)/character_limit))
        uuid_val = uuid.uuid4()
        time = datetime.utcnow().replace(tzinfo=timezone.utc)
        for x in range(0, part_num):
            text = msg[0+character_limit*x:character_limit*(x+1)]
            print("[{}] - [{}] [{}] [{}]: {}".format(str(time), tag, uuid_val, "{}/{}".format(x+1, part_num), text), flush=True)

def find_leaf_parents(competencies: List[Competency], cass_graph: CassGraph):
    leaf_parents = dict()
    for competency in competencies:
        if cass_graph.is_leaf(competency):
            leaf_parent = cass_graph.get_parent_competency(competency)
            if leaf_parent.id not in leaf_parents:
                leaf_parents[leaf_parent.id] = leaf_parent

    return list(leaf_parents.values())


def get_lowest_leaf_parents(leaf_parents: List[Competency], cass_graph: CassGraph):
    novice = list()
    intermediate = list()
    expert = list()
    for parent in leaf_parents:
        if cass_graph.get_previous_neighbor(parent) == None:
            novice.append(parent)
        elif cass_graph.get_next_neighbor(parent) == None:
            expert.append(parent)
        else:
            intermediate.append(parent)

    if len(novice) > 0:
        return novice
    elif len(intermediate) > 0:
        return intermediate
    else:
        return expert


def get_target_leaf_parent_by_mastery_prob(leaf_parents: List[Competency], learner: Learner) -> Competency:
    mastery_probabilities = learner.mastery_probabilities
    target_leaf_parent = None
    target_leaf_parent_mp = None
    for competency in leaf_parents:
        mp = get_most_recent_mastery_probability(mastery_probabilities, competency.id)
        if target_leaf_parent == None:
            target_leaf_parent = competency
            target_leaf_parent_mp = mp
        elif target_leaf_parent_mp == None or (mp is not None and target_leaf_parent_mp.probability < mp.probability):
            target_leaf_parent = competency
            target_leaf_parent_mp = mp

    return target_leaf_parent


def get_most_recent_mastery_probability(mastery_probabilities: List[MasteryProbability], competencyId: str):
    return_mastery = None
    for mp in mastery_probabilities:
        if target_url_equals_competency(mp.competency_id, competencyId):
            if return_mastery == None:
                return_mastery = mp
            elif return_mastery.timestamp < mp.timestamp:
                return_mastery = mp

    return return_mastery


def get_new_subgoals(old_subgoals: List[Competency], target_leaf_parent: Competency, cass_graph: CassGraph):
    return_list = list()
    old_subgoal_ids = [subgoal.id for subgoal in old_subgoals]
    return_list.append(target_leaf_parent)
    children = cass_graph.get_children(target_leaf_parent)
    if children != None:
        for child in children:
            if child.id in old_subgoal_ids:
                return_list.append(child)

    parent = cass_graph.get_parent_competency(target_leaf_parent)
    while parent != None:
        if parent.id in old_subgoal_ids:
            return_list.insert(0, parent)

        parent = cass_graph.get_parent_competency(parent)

    return return_list
