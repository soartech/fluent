from learner_inferences_server.amqp_listener.inference_utils import recursivelyConvertTimestampsInDict
from learner_inferences_server.config import Config
from itertools import groupby

from learner_inferences_server.amqp_listener.mastery_calculators.weighted_avg_mastery_calculator import WeightedAvgMasteryCalculator

SAVE_RESULTS = True

# TODO: Move these to Config and update uses accordingly when possible.
MIN_REQUIRED_OBSERVATIONS = 1
MASTERY_PROB_THRESHOLD = 0.8

def get_all_learners():
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    required_props = {'name': 1,
                      'identifier': 1,
                      'masteryEstimates': 1,
                      'masteryProbabilities': 1,
                      'pastMasteryEstimates': 1
                      }
    learner_list = store.get_learners_with_properties(required_props)
    return learner_list

def get_one_learner_by_id(learner_id):
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    required_props = {'name': 1,
                      'identifier': 1,
                      'masteryEstimates': 1,
                      'masteryProbabilities': 1,
                      'pastMasteryEstimates': 1
                      }
    learner = store.get_learner_properties(learner_id, required_props)
    if learner is None:
        return []
    else:
        return [learner]

def get_all_learners_requests():
    import requests
    response = requests.get("insertIPAddr/learner-inferences/learners")
    return response.json()

def update_mastery_estimates_for_all(learners):
    for learner in learners:
        if 'masteryProbabilities' in learner and learner['masteryProbabilities'] != None:
            learner = get_mastery_estimates(learner)
            update_learner(learner)


def get_mastery_estimates(learner):
    mastery_probabilities = learner.get('masteryProbabilities', [])
    if len(mastery_probabilities) > 0:
        mastery_probabilities.sort(key=lambda x:x['competencyId'])
        for key, value in groupby(mastery_probabilities, key=lambda x:x['competencyId']):
            competency_mps = list(value)
            mastery_calculator = WeightedAvgMasteryCalculator(MIN_REQUIRED_OBSERVATIONS, MASTERY_PROB_THRESHOLD)
            new_mastery_estimate = mastery_calculator.calc_mastery_estimate(competency_mps, key)
            learner = update_mastery_estimate_in_learner(learner, new_mastery_estimate)

    return learner

def update_mastery_estimate_in_learner(learner, new_estimate):
    estimateToUpdate = None
    for estimate in learner['masteryEstimates']:
        if new_estimate['competencyId'] == estimate['competencyId']:
            estimateToUpdate = estimate
            break
    if estimateToUpdate is not None:
        if 'pastMasteryEstimates' not in learner or learner['pastMasteryEstimates'] == None:
            learner['pastMasteryEstimates'] = []
        learner['pastMasteryEstimates'].append(estimateToUpdate)
        learner['masteryEstimates'].remove(estimateToUpdate)

    learner['masteryEstimates'].append(new_estimate)

    return learner

def update_learner(learner):
    if SAVE_RESULTS:
        store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
        learner_update_dict = {"masteryEstimates": learner['masteryEstimates'], "pastMasteryEstimates": learner['pastMasteryEstimates']}
        learner_update_dict = recursivelyConvertTimestampsInDict(learner_update_dict)
        store.update_learner(learner['identifier'], learner_update_dict)
    else:
        print(learner['masteryEstimates'], learner['pastMasteryEstimates'])


if __name__ == "__main__":
    if Config.USE_MASTERY_DECAY:
        learners = get_all_learners()
        update_mastery_estimates_for_all(learners)
