from bson import ObjectId

import learner_inferences_server.amqp_listener.inference_utils as fns
from learner_inferences_server.config import Config
from learner_inferences_server.amqp_listener.mastery_calculators.simple_mastery_calculator import SimpleMasteryCalculator


# TODO: This test needs to be updated to latest change: classes to calculate mastery estimates instead of funcs.
def test_calc_mastery_estimate():
    print('Testing _calc_mastery_estimate:')
    LEARNER_ID = '3e034888-6d6b-4096-8570-b50a21be9cc4'

    mastery_prob = {
        '@context': 'sampleContext',
        '@type': Config.AMQP_MASTERY_PROB_TYPE,
        'learnerId': LEARNER_ID,
        'timestamp': '2018-07-19T14:44:00.320Z',
        'competencyId': 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037',
        'probability': 0.75,
        'confidence': 0.97,
        'source': 'CASS'
    }
    mastery_calculator = SimpleMasteryCalculator(Config.MASTERY_THRESHOLDS)
    newEstimate = mastery_calculator.calc_mastery_estimate([mastery_prob], mastery_prob['competencyId'])
    print(newEstimate)

    # assert(estimate['@context'] == 'sampleContext')
    # assert(estimate['competencyId'] == 'http:/competencynuggets.com/12049823409823')
    # assert(estimate['timestamp'] == 'John 3:16')
    #
    # inference = {
    #     '@context': 'otherContext',
    #     '@type': Config.AMQP_MASTERY_PROB_TYPE,
    #     'learnerId': '999',
    #     'timestamp': 'Thursday at 9:00',
    #     'competencyId': 'http:/competencynuggets.com/252625545',
    #     'nextAttempt': 2,
    #     'masteryProbability': 0.47,
    #     'confidence': 0.01
    # }
    # # Test that other values are not copied from inference to mastery
    # estimate = fns._calc_mastery_estimate(inference)
    # assert(estimate['@context'] == 'otherContext')
    # assert(estimate['@type'] == Config.AMQP_MASTERY_ESTIMATE_TYPE)
    # assert(estimate['mastery'] == 'forgotten')
    # assert('learnerId' not in estimate)
    # assert('nextAttempt' not in estimate)
    # assert('masteryProbability' not in estimate)
    # assert('confidence' not in estimate)

    # print('All assertions passed.')
    # print()


# TODO: Needs updates to current mastery levels (novice, intermediate, expert).
# def test_get_mastery_estimate():
#     print('Testing _get_mastery_estimate:')
#
#     learnerDict = {
#         '@context': 'someWeirdContext',
#         '@type': 'Learner',
#         'identifier': 'https://learner-profile-service/learners/7799803df3f4948bd2f98317',
#         'name': 'Hot Diggity Dawg',
#         'masteryEstimates': [
#             {
#              '@context': 'someWeirdContext',
#              '@type': 'MasteryEstimate',
#              'competencyId': 'http://CASS.com/345082374591',
#              'mastery': 'forgotten',
#              'timestamp': '19:19:19:19'
#             },
#             {
#              '@context': 'someWeirdContext',
#              '@type': 'MasteryEstimate',
#              'competencyId': 'http://CASS.com/56709759862234346',
#              'mastery': 'held',
#              'timestamp': '1234:09'
#             }
#         ],
#         'pastMasteryEstimates':[
#             {
#              '@context': 'someWeirdContext',
#              '@type': 'MasteryEstimate',
#              'competencyId': 'http://CASS.com/66666645748348',
#              'mastery': 'held',
#              'timestamp': 'Yesterday'
#             }
#         ],
#         'masteryProbabilities':[
#             {
#              '@context': 'someWeirdContext',
#              '@type': 'MasteryProbability',
#              'competencyId': 'http://CASS.com/12343679675353',
#              'probability': -0.6,
#              'timestamp': 'Timestamp'
#             },
#             {
#              '@context': 'someWeirdContext',
#              '@type': 'MasteryProbability',
#              'competencyId': 'http://CASS.com/1010102383848',
#              'probability': 0.99999,
#              'timestamp': '2018-04-05T104:41:01'
#             }
#         ]
#     }
#
#     inference = {
#         '@context': 'otherContext',
#         '@type': Config.AMQP_MASTERY_PROB_TYPE,
#         'learnerId': '59',
#         'timestamp': '24:01:00',
#         'competencyId': 'http://CASS.com/345082374591',
#         'nextAttempt': 2,
#         'masteryProbability': 0.777,
#         'confidence': 0.555
#     }
#     # Test that certain values are copied from inference to mastery,
#     # a mastery is updated (not added) when the inference competency id exists in learnerDict,
#     # and a pastMasteryEstimate is added when masteryEstimate is replaced,
#     newEstimate, updatedDict = fns._get_mastery_estimate(learnerDict, inference)
#     assert(newEstimate['competencyId'] == 'http://CASS.com/345082374591')
#     assert(newEstimate['timestamp'] == '24:01:00')
#     assert(len(updatedDict['masteryEstimates']) == 2)
#     assert(len(updatedDict['pastMasteryEstimates']) == 2)
#     assert(updatedDict['pastMasteryEstimates'][1]['timestamp'] == '19:19:19:19')
#
#     inference = {
#         '@context': 'otherContext',
#         '@type': Config.AMQP_MASTERY_PROB_TYPE,
#         'learnerId': '59',
#         'timestamp': 'Never',
#         'competencyId': 'http://CASS.com/abcde12345',
#         'nextAttempt': 10,
#         'masteryProbability': 0.381,
#         'confidence': 0.209
#     }
#     # Test that a mastery is added when the inference competency id doesn't exist in learnerDict,
#     # and a pastMasteryEstimate is not added when a new masteryEstimate is added
#     newEstimate, updatedDict = fns._get_mastery_estimate(learnerDict, inference)
#     assert(len(updatedDict['masteryEstimates']) == 3)
#     assert(len(updatedDict['pastMasteryEstimates']) == 2)
#     assert(updatedDict['masteryEstimates'][2]['timestamp'] == 'Never')
#
#     print('All assertions passed.')
#     print()


def test_get_id_from_learnerId():
    print('Testing get_id_from_learnerId:')
    
    # Test that the value after the last slash is stored as the learnerId
    learnerId = 'http://iamapizza/oink/130498340'
    assert(fns.get_id_from_learnerId(learnerId) == '130498340')
    learnerId = 'whyaretheresomanyslashes//////////09458232340/22138434'
    assert(fns.get_id_from_learnerId(learnerId) == '22138434')
    
    print('All assertions passed.')
    print()

# TODO: Needs updates to current mastery levels (novice, intermediate, expert).
# def test_process_mastery_prob():
#     print('Testing process_mastery_prob:')
#
#     LEARNER_ID = '3e034888-6d6b-4096-8570-b50a21be9cc4'
#
#     # Create Learner in store from scratch.
#     database = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
#     if database.get_learner(LEARNER_ID) is not None:
#         database.delete_learner(LEARNER_ID)
#
#     database.save_learner({
#         "@context": "tla-declarations.jsonld",
#         "@type": "Learner",
#         "identifier": LEARNER_ID,
#         "name": "Fluent Test",
#         "email": "fluent-test@soartech.com",
#         "activityAttemptCounters": [],
#         "bored": False,
#         "competencyAchievements": [],
#         "competencyAttemptCounters": [],
#         "confused": False,
#         "currentActivities": [],
#         "currentDeviceCategories": [],
#         "currentPlatforms": [],
#         "eureka": False,
#         "flow": False,
#         "frustrated": False,
#         "goals": [],
#         "lastActivityHard": False,
#         "lastActivityUseful": False,
#         "mainEntityOfPage": "string",
#         "masteryEstimates": [{
#             "@context": "context123",
#             "@type": "MasteryEstimate",
#             "competencyId": 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037',
#             "mastery": "not held", #Should become held when inference processed below.
#             "timestamp": "2018-07-19T14:05:00.930Z"
#         }],
#         "masteryProbabilities": [],
#         "competencyAttemptCounters": [],
#         "pastGoals": [],
#         "pastMasteryEstimates": [],
#         "sleepy": False
#     })
#
#     inference = {
#         '@context': 'context123',
#         '@type': Config.AMQP_MASTERY_PROB_TYPE,
#         'learnerId': LEARNER_ID,
#         'timestamp': '2018-07-19T14:44:00.320Z',
#         'competencyId': 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037',
#         'nextAttempt': 1,
#         'masteryProbability': 0.825,
#         'confidence': 0.5,
#         'source': 'AFM'
#     }
#     # Test that a new inference is not created if the learner does not exist in the database
#     newInference = fns.process_mastery_prob(inference)
#     assert(len(newInference) != 0)
#
#     learnerDict = {
#         '_id': ObjectId('5aecab7cb72f7717887cc5fb'),
#         '@context': 'someWeirdContext',
#         '@type': 'Learner',
#         'identifier': LEARNER_ID,
#         'name': 'Santa Claus',
#         'currentDeviceCategories': ['Laptop', 'iPad'],
#         'currentPlatforms': ['Web', 'IOS']
#     }
#     # Test that after a new learner is added to the database and a new inference is created
#     # with that learner's ID, that learner stores a new masteryEstimate and masteryProbability;
#     # also test that certain data is copied from raw inference to final inference, and
#     # the new inference contains the correct mastery estimate
#     database.save_learner(learnerDict, 'https://learner-profile-service/learners')
#     newInference = fns.process_mastery_prob(inference)
#
#     required_props = {'name': 1,
#                       'masteryEstimates': 1,
#                       'masteryProbabilities': 1,
#                       'pastMasteryEstimates': 1
#     }
#
#     # Properties not in DB should be returned as None.
#     learnerInDatabase = database.get_learner_properties(LEARNER_ID, required_props)
#
#     assert(len(learnerInDatabase['masteryEstimates']) == 1)
#     assert(learnerInDatabase['masteryEstimates'][0]['competencyId'] == 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037')
#     assert(len(learnerInDatabase['masteryProbabilities']) == 1)
#     assert(learnerInDatabase['masteryProbabilities'][0]['probability'] == 0.825)
#     assert('pastMasteryEstimates' not in learnerInDatabase)
#     assert(newInference['@context'] == 'context123')
#     assert(newInference['@type'] == Config.AMQP_LEARNER_INFERENCE_TYPE)
#     assert(newInference['learnerId'] == LEARNER_ID)
#     assert(newInference['masteryEstimates']['competencyId'] == 'https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037')
#
#     print('All assertions passed.')
#     print()


def main():
    print()
    test_calc_mastery_estimate()
    # test_get_mastery_estimate()
    # test_get_id_from_learnerId()
    # test_process_mastery_prob()


if __name__ == '__main__':
    main()
