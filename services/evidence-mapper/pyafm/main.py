import json
import math
import csv
import pickle
import uuid
import os.path
from threading import Thread
import traceback

from basic_estimators import BasicColdStartMasteryEstimator
from util import get_competency_attempt_counters
from config import AFM_ENABLED, TRANSFER_LEARNING_ENABLED, BCSE_ENABLED

# TODO: This dependency on learner_inference should be removed, as they are very different concerns.
from learner_inferences_server.amqp_listener import inference_utils

from competency_attempts_collector import CompetencyAttemptsCollector
from mastery_estimators.afm_estimators import AFMOnlineMasteryEstimator
from mastery_estimators.uc_davis_estimators import OptimizedOnlineTransferMasteryEstimator
from util import print_with_time

dir_path = os.path.dirname(os.path.realpath(__file__))


def run_afm(statements):
    print(len(statements))
    afm_id = uuid.uuid4()
    num_divs = 1000
    statement_len = len(statements)
    statements_div = math.floor(statement_len / num_divs)

    with open('outfile_{}.csv'.format(num_divs), 'w', newline='\n') as csvfile:
        fieldnames = ['learner', 'competency', 'prob_proficiency', 'attempts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(0, num_divs):
            if x == num_divs - 1:
                test_statements = statements[statements_div*x:statement_len]
            else:
                test_statements = statements[statements_div*x:statements_div*(x+1)]

            if (x+1) % 100 == 0:
                print("{}/{} batches completed".format(x+1, num_divs))

            predictions = train_and_predict(afm_id, test_statements)

            for pred in predictions:
                writer.writerow(pred)


def train_and_predict(study_id, test_statements):
    train_data = CompetencyAttemptsCollector().get_competency_attempts(test_statements)

    predictions_afm = list()
    predictions_transfer_learning = list()
    predictions_bcse = list()

    if len(train_data) > 0:
        # Populate competency_attempt_counters in advance.
        competency_attempt_counters = {}
        for learner_id, competency_dict in train_data.items():
            # Need to use list to be 100% sure we're not modifying the dict while iterating
            for competency_id in list(competency_dict.keys()):
                competency_dict[inference_utils.sanitize_competency_id(competency_id)] = competency_dict.pop(competency_id)
            if learner_id not in competency_attempt_counters:
                competency_attempt_counters[learner_id] = {}
            for competency_id in competency_dict.keys():
                try:
                    attempt_counter = get_competency_attempt_counters(learner_id, competency_id)
                except Exception as e:
                    print_with_time('ERROR: ' + traceback.format_exc())
                    attempt_counter = None

                if attempt_counter is None:
                    competency_attempt_counters[learner_id][competency_id] = 0
                else:
                    competency_attempt_counters[learner_id][competency_id] = attempt_counter['numAttempts']

        if AFM_ENABLED:
            afm_thread = Thread(target=_train_and_predict_afm,
                                           args=(study_id, train_data, competency_attempt_counters, predictions_afm))
            afm_thread.start()

        if TRANSFER_LEARNING_ENABLED:
            transfer_learning_thread = Thread(target=_train_and_predict_transfer_learning,
                                        args=(study_id, train_data, competency_attempt_counters, predictions_transfer_learning))
            transfer_learning_thread.start()

        if BCSE_ENABLED:
            bcse_thread = Thread(target=_train_and_predict_bcse,
                                 args=(study_id, train_data, competency_attempt_counters, predictions_bcse))
            bcse_thread.start()

        if AFM_ENABLED:
            afm_thread.join()
        if TRANSFER_LEARNING_ENABLED:
            transfer_learning_thread.join()
        if BCSE_ENABLED:
            bcse_thread.join()

    return predictions_afm + predictions_transfer_learning + predictions_bcse

def _train_and_predict_afm(study_id, train_data, competency_attempt_counters, predictions):
    # TODO: To improve performance, load the models at service startup and keep them in memory.
    #       Storing models after each train is still needed to cover for potential system crashes.
    try:
        afm, afm_estimator_filename = _retrieve_afm_estimator(study_id)
        afm.train(train_data)
        predictions.extend(afm.predict_next(train_data))
        afm.update_stored_data(train_data)
        for i, pred in enumerate(predictions):
            learner_id = pred['learnerId']
            competency_id = inference_utils.sanitize_competency_id(pred['competencyId'])
            predictions[i]['nextAttempt'] = competency_attempt_counters[learner_id][competency_id] + 1
            predictions[i]['@type'] = 'MasteryProbability'

        pickle.dump(afm, open(afm_estimator_filename, "wb"))
    except Exception as e:
        print_with_time('ERROR: ' + traceback.format_exc())

def _train_and_predict_transfer_learning(study_id, train_data, competency_attempt_counters, predictions):
    # TODO: To improve performance, load the models at service startup and keep them in memory.
    #       Storing models after each train is still needed to cover for potential system crashes.
    try:
        online_transfer, online_transfer_file = _retrieve_online_transfer_estimator(study_id)
        online_transfer.train(train_data)
        predictions.extend(online_transfer.predict(train_data))
        for i, pred in enumerate(predictions):
            learner_id = pred['learnerId']
            competency_id = inference_utils.sanitize_competency_id(pred['competencyId'])
            predictions[i]['nextAttempt'] = competency_attempt_counters[learner_id][competency_id] + 1
            predictions[i]['@type'] = 'MasteryProbability'

        pickle.dump(online_transfer, open(online_transfer_file, "wb"))
    except Exception as e:
        print_with_time('ERROR: ' + traceback.format_exc())

def _train_and_predict_bcse(study_id, train_data, competency_attempt_counters, predictions):
    try:
        predictions.extend(BasicColdStartMasteryEstimator().predict(train_data))
        for i, pred in enumerate(predictions):
            learner_id = pred['learnerId']
            competency_id = inference_utils.sanitize_competency_id(pred['competencyId'])
            predictions[i]['nextAttempt'] = competency_attempt_counters[learner_id][competency_id] + 1
            predictions[i]['@type'] = 'MasteryProbability'
    except Exception as e:
        print_with_time('ERROR: ' + traceback.format_exc())

def _retrieve_afm_estimator(study_id):
    afm_estimator_filename = dir_path + "/saved_estimators/{}_afm.pkl".format(study_id)
    if os.path.isfile(afm_estimator_filename):
        afm = pickle.load(open(afm_estimator_filename, "rb"))
    else:
        afm = AFMOnlineMasteryEstimator()
    return afm, afm_estimator_filename

def _retrieve_online_transfer_estimator(study_id):
    online_transfer_filename = dir_path + "/saved_estimators/{}_online_transfer_learning.pkl".format(study_id)
    if os.path.isfile(online_transfer_filename):
        online_transfer = pickle.load(open(online_transfer_filename, "rb"))
    else:
        online_transfer = OptimizedOnlineTransferMasteryEstimator()
    return online_transfer, online_transfer_filename


if __name__ == "__main__":
    import os
    try:
        os.remove("example_learner_data.json")
    except:
        pass

    try:
        os.remove("./saved_estimators/fluent_afm.pkl")
    except:
        pass

    try:
        os.remove("./saved_estimators/fluent_online_transfer_learning.pkl")
    except:
        pass

    with open('xapi_statements_fluent.json', 'r') as infile:
        xapi_statements = json.load(infile)


    # TODO: Find out why processing multiple statements at once work, but not code below that runs one at a time (AFM error).
    # print(train_and_predict('fluent', xapi_statements))
    # print("---")

    # statements = [{"version": "1.0.0", "id": "7df5a88b-a527-11e7-93e8-9cb6d063d611", "actor": {"objectType": "Agent", "name": "D80FD", "account": {"name": "D80FD", "homePage": "https://pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=263"}}, "verb": {"id": "http://adlnet.gov/expapi/verbs/passed", "display": {"en-US": "passed"}}, "object": {"objectType": "Activity", "id": "https://pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=263/step/%28BODY%20SWIMMER%29"}, "context": {"contextActivities": {"parent": [{"objectType": "Activity", "id": "https://pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=263/problem/VEC1A"}], "grouping": [{"objectType": "Activity", "id": "https://pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=263/problem/VEC1A"}]}, "extensions": {"http://www.soartech.com/target/learnsphere-transaction-id": "436fd8ae3a41f4646677b3071f23d37a", "http://www.soartech.com/target/competencies": [{"competencyId": "http://insertCassUrl/api/custom/data/insertCassSchemaUrl.0.2.Competency/pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=263/Default/DRAW-BODY", "framework": "Default"}]}}, "result": {"duration": "PT2.4S", "success": True}, "timestamp": "2008-09-10T00:50:52+00:00", "authority": {"objectType": "Agent", "name": "API Client", "mbox": "mailto:api_client@soartech.com"}, "stored": "2017-09-29T15:40:50.986800+00:00"}]
    for statement in xapi_statements:
        print_with_time(train_and_predict('fluent', [statement]))
        print("---")
    #run_afm(statements)
