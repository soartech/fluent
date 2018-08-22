import requests
from cass_graph_client.cass_graph import CassGraph
from cass_client import Competency
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.utils import load_or_instantiate, has_challenge_level, MagicStrings, get_aligned_elo
from learner_inferences_client.models import Learner
from datetime import datetime, timezone
from typing import Optional, List
from activity_index_client.models import LearningActivity
import json

UPDATE_LEARNER = False
UPDATE_THROUGH_ELO = False
UPDATE_THROUGH_TLO = True
SET_GOAL = False


CLEAR_DATA = {
    "activityAttemptCounters": [],
    "competencyAchievements": [],
    "competencyAttemptCounters": [],
    "goals": [],
    "masteryEstimates": [],
    "masteryProbabilities": [],
    "pastGoals": [],
    "pastMasteryEstimates": [],
    "bored": False,
    "confused": False,
    "eureka": False,
    "flow": False,
    "frustrated": False,
    "lastActivityHard": False,
    "lastActivityUseful": False,
    "sleepy": False
}

learner_inferences_url = "insertIPAddr/learner-inferences/learners"


def get_learner_id_by_name(name_target: str) -> Optional[str]:
    learners_response = requests.get("insertIPAddr/learner-inferences/learners")

    for learner in learners_response.json():
        name = learner.get('name', None)
        if name == name_target:
            return learner.get('identifier', None)


def mastery_estimate_generator(competency_id: str, mastery: str) -> dict:
    return {
        "@context": "tla-declarations.jsonld",
        "@type": "MasteryEstimate",
        "competencyId": competency_id,
        "mastery": mastery,
        "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    }

def competency_attempt_generator(competency_id: str) -> dict:
    return {
        "@context": "tla-declarations.jsonld",
        "@type": "CompetencyAttemptCounter",
        "attempts": 1,
        "competencyId": competency_id,
        "lastAttemptDateTime": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    }

def clear_learner_patch(learner: Learner):
    if learner.identifier is not None:
        print("Clearing learner {} of temporal data".format(learner_id))
        patch_learner(learner_id, CLEAR_DATA)


def patch_learner(learner_id: str, learner_patch_json: dict):
    if UPDATE_LEARNER:
        response = requests.patch(learner_inferences_url+"/"+learner_id, json=learner_patch_json)
        print(response.json())
    else:
        print(json.dumps(learner_patch_json, indent=4))


def master_up_through_tlo(tlo_ceasncoded_notation: str, cass_graph: CassGraph, learner: Learner) -> Optional[Competency]:
    tlo = cass_graph.get_first_top_level_competency()
    competency_attempts = []
    mastery_estimates = []
    while tlo is not None:
        elos = cass_graph.get_children_ordered(tlo)
        for elo in elos:
            elo_id = elo.id
            competency_attempts.append(competency_attempt_generator(elo_id))
            mastery_estimates.append(mastery_estimate_generator(elo_id, 'held'))
        tlo_id = tlo.id
        competency_attempts.append(competency_attempt_generator(tlo_id))
        mastery_estimates.append(mastery_estimate_generator(tlo_id, 'held'))
        if tlo.ceasncoded_notation == tlo_ceasncoded_notation:
            break

        tlo = cass_graph.get_next_neighbor(tlo)

    patch_learner(learner.identifier, {
        "competencyAttemptCounters": competency_attempts,
        "masteryEstimates": mastery_estimates
    })

    return tlo


def set_goal_to_next_elo(tlo: Competency, learner: Learner):
    if tlo is not None:
        next_tlo = cass_graph.get_next_neighbor(tlo)
        children = cass_graph.get_children_ordered(next_tlo)
        goal = []

        while children is not None and len(children) > 0:
            first_elo = children[0]
            children = cass_graph.get_children_ordered(first_elo)
            if children is not None and len(children) > 0:
                goal = [{
                    "@context": "tla-declarations.jsonld",
                    "@type": "Goal",
                    "competencyId": first_elo.id
                }]

        patch_learner(learner.identifier, {
            "goals": goal
        })


def strip_list_str(val: str) -> str:
    val = val.replace('[', '').replace(']', '').replace("'", "")
    return val


def master_up_through_elo(elo_ceasncoded_notation: str, cass_graph: CassGraph, learner: Learner):
    tlo = cass_graph.get_first_top_level_competency()
    competency_attempts = []
    mastery_estimates = []
    last_mastered_elo = None
    while tlo is not None:
        elos = cass_graph.get_children_ordered(tlo)
        for elo in elos:
            elo_id = elo.id
            elo_children = cass_graph.get_children_ordered(elo)
            if elo_children is not None:
                for elo_child in elo_children:
                    child_id = elo_child.id
                    competency_attempts.append(competency_attempt_generator(child_id))
                    print(elo_child.ceasncoded_notation)
                    mastery_estimates.append(mastery_estimate_generator(child_id, 'held'))
                    if elo_child.ceasncoded_notation == elo_ceasncoded_notation:
                        last_mastered_elo = elo_child
                        break

            if last_mastered_elo is None:
                print(elo.ceasncoded_notation)
                competency_attempts.append(competency_attempt_generator(elo_id))
                mastery_estimates.append(mastery_estimate_generator(elo_id, 'held'))
                if elo.ceasncoded_notation == elo_ceasncoded_notation:
                    last_mastered_elo = elo
                    break

        if last_mastered_elo is not None:
            break
        print(tlo.ceasncoded_notation)
        tlo_id = tlo.id
        competency_attempts.append(competency_attempt_generator(tlo_id))
        mastery_estimates.append(mastery_estimate_generator(tlo_id, 'held'))

        tlo = cass_graph.get_next_neighbor(tlo)

    patch_learner(learner.identifier, {
        "competencyAttemptCounters": competency_attempts,
        "masteryEstimates": mastery_estimates
    })

    return last_mastered_elo



def handle_activities(activities: List[LearningActivity]):
    for activity in activities:
        aligned_elo_id = get_aligned_elo(activity)
        if activity.interactivity_type == "Passive" and has_challenge_level(aligned_elo_id, activity, MagicStrings.ChallengeLevels.SIMPLE):
            print(activity.metadata_file)

if __name__ == "__main__":
    query_cacher = QueryCacher()
    learner_id = get_learner_id_by_name("Fluent Three")
    learner, etag = query_cacher.get_learner(learner_id)

    if UPDATE_LEARNER:
        print("About to clear data for learner '{}', with ID {}.".format(learner.name, learner.identifier))
        confirmation = input("Proceed (yes/no)? ")
    else:
        print("Will print out what call payloads would be. Note: NO UPDATING IS HAPPENING.")
        confirmation = "yes"

    if confirmation == "yes":
        clear_learner_patch(learner)
        cass_graph = load_or_instantiate('recommenderserver.resources', CassGraph, '59e884bb-510b-4f36-8443-8c3842336e28') # type: CassGraph

        if UPDATE_THROUGH_TLO:
            last_mastered_tlo = master_up_through_tlo("3", cass_graph, learner)

            if SET_GOAL:
                # Assuming that the UI is setting this goal. Is this accurate?
                set_goal_to_next_elo(last_mastered_tlo, learner)

        if UPDATE_THROUGH_ELO:
            last_mastered_elo = master_up_through_elo('3.1', cass_graph, learner)

    else:
        print("Aborted.")
