import connexion
import six
import requests
from requests.auth import HTTPBasicAuth
import dateutil.parser
from datetime import timezone

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from swagger_server.models.activity_response import ActivityResponse
from swagger_server.models.error import Error
from swagger_server import util
from swagger_server.config import Config, LRSConfig
from swagger_server.encoder import JSONEncoder

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]
selfReportId = None

NUM_LEARNER_PATCH_RETRIES = 10


def delete_activity_response(activityId):
    """
    Removes the activity and all responses associated with it from the database

    :param activityId: The ID of the activity to delete
    :type activityId: str
    :rtype: None
    """
    
    activityResponseDict = db.activity_responses.find_one({'activityId': activityId}, {'_id': 0})
    if activityResponseDict is None:
        return 'Activity response and paradata for activity with ID ' + activityId + ' does not exist'
    db.activity_responses.remove({'activityId': activityId})
    db.activity_paradata.remove({'activityId': activityId})
    return 'Activity response and paradata successfully removed'


def determineTraits(paradataDict):
    activityTraits = {}
    mostCommonEmotion = 'neutral'
    mostCommonEmotionCount = paradataDict['neutralCount']
    
    activityTraits['popularityRating'] = paradataDict['popularityRatingSum'] / paradataDict['responseCount']
    
    if (paradataDict['boringCount'] > mostCommonEmotionCount):
        mostCommonEmotion = 'boring'
        mostCommonEmotionCount = paradataDict['boringCount']
    if (paradataDict['confusingCount'] > mostCommonEmotionCount):
        mostCommonEmotion = 'confusing'
        mostCommonEmotionCount = paradataDict['confusingCount']
    if (paradataDict['frustratingCount'] > mostCommonEmotionCount):
        mostCommonEmotion = 'frustrating'
        mostCommonEmotionCount = paradataDict['frustratingCount']
    if (paradataDict['flowCount'] > mostCommonEmotionCount):
        mostCommonEmotion = 'flow'
        mostCommonEmotionCount = paradataDict['flowCount']
    if (paradataDict['eurekaCount'] > mostCommonEmotionCount):
        mostCommonEmotion = 'eureka'
    
    activityTraits['emotionRating'] = mostCommonEmotion

    return activityTraits


def getSelfReportActivityId():
    # Obtain ID for self-report activity to use in xAPI statement
    url = Config.ACTIVITY_INDEX_ENDPOINT
    response = requests.get(url)
    if response.status_code == 200:
        for activity in json.loads(response.text):
            if 'educationalUse' in activity and 'SelfReport' in activity['educationalUse']:
                return activity['identifier']
    return ''


def getMostRecentActivityId(id):
    # Obtain ID for most recently completed Activity so self-report can be linked with correct activity
    url = Config.LEARNER_INFERENCES_ENDPOINT + '/' + id
    response = requests.get(url)
    if response.status_code == 200:
        learnerInfo = json.loads(response.text)
        if 'activityAttemptCounters' in learnerInfo and len(learnerInfo['activityAttemptCounters']) > 0:
            attempt_counters = learnerInfo['activityAttemptCounters']
            return max(attempt_counters, key=lambda x: \
                dateutil.parser.parse(x['lastAttemptDateTime']).replace(tzinfo=timezone.utc))['activityId']
    return ''


def getLearnerName(id):
    # Obtain name for learner to use in xAPI statement
    url = Config.LEARNER_INFERENCES_ENDPOINT + '/' + id
    response = requests.get(url)
    if response.status_code == 200:
        learnerDict = json.loads(response.text)
        if 'name' in learnerDict:
            return learnerDict['name']
    return 'Unknown Learner'


def post_activity_response(activityResponseObj):
    """
    Adds a new activity response to the database; if this is the first activity response for the activity, also adds the activity to the database

    :param activityResponseObj: ActivityResponse object to add
    :type activityResponseObj: dict | bytes
    :rtype: None
    """
    
    activityResponseObj = ActivityResponse.from_dict(connexion.request.get_json())
    activityResponseDict = JSONEncoder().default(activityResponseObj)
    activityResponseDict['activityId'] = getMostRecentActivityId(activityResponseDict['learnerKeycloakId'])
    activityId = activityResponseDict['activityId']
    if activityId == '':
        return "Error: unable to retreive learner's most recent activity"

    db.activity_responses.insert_one(activityResponseDict)
    returnString = 'New activity response created for activity with ID ' + activityId + '  '
    
    activityParadataDict = {}
    
    # Prepare to add paradata counts
    activityParadataDict['responseCount'] = 1
    activityParadataDict['popularityRatingSum'] = activityResponseDict['popularityRating']
    activityParadataDict['boringCount'] = 0
    activityParadataDict['confusingCount'] = 0
    activityParadataDict['frustratingCount'] = 0
    activityParadataDict['flowCount'] = 0
    activityParadataDict['eurekaCount'] = 0
    activityParadataDict['neutralCount'] = 0
    activityParadataDict[activityResponseDict['emotionRating'] + 'Count'] = 1
    
    # Create or update paradata using new response data
    activityParadata = db.activity_paradata.find_one({'activityId': activityId}, {'_id': 0})
    if activityParadata is None:
        activityParadataDict['activityId'] = activityResponseDict['activityId']
        db.activity_paradata.insert_one(activityParadataDict)
        returnString += 'New activity paradata created  '
    else:
        db.activity_paradata.update({'activityId': activityId}, {'$inc': activityParadataDict})
        returnString += 'Activity paradata updated  '

    # Calculate activity traits using paradata thresholds
    activityParadata = db.activity_paradata.find_one({'activityId': activityId}, {'_id': 0})
    activityTraits = determineTraits(activityParadata)

    # PATCH activity traits to Activity Index service
    updateSuccess = True
    headers = {'content-type': 'application/json'}
    url = Config.ACTIVITY_INDEX_ENDPOINT + '/' + activityId
    response = requests.patch(url, data = json.dumps(activityTraits), headers = headers)
    if response.status_code != 200:
        updateSuccess = False
    returnString += 'Response from Activity Index service: ' + response.text + '  '

    # Prepare learner trait data to be PATCHed to Learner Inferences service
    learnerTraitData = {}
    learnerTraitData['identifier'] = activityResponseDict['learnerKeycloakId']
    if activityResponseDict['emotionRating'] == 'boring':
        learnerTraitData['bored'] = True
    elif activityResponseDict['emotionRating'] == 'confusing':
        learnerTraitData['confused'] = True
    elif activityResponseDict['emotionRating'] == 'frustrating':
        learnerTraitData['frustrated'] = True
    elif activityResponseDict['emotionRating'] == 'flow':
        learnerTraitData['flow'] = True
    elif activityResponseDict['emotionRating'] == 'eureka':
        learnerTraitData['eureka'] = True

    url = Config.LEARNER_INFERENCES_ENDPOINT + '/' + learnerTraitData['identifier']

    # PATCH learner trait data to Learner Inferences service
    for i in range(NUM_LEARNER_PATCH_RETRIES):
        response = requests.get(url)
        etag = response.headers['ETag']
        headers = {'content-type': 'application/json', 'if-match': etag}
        response = requests.patch(url, data = json.dumps(learnerTraitData), headers = headers)
        if response.status_code == 200:
            learnerInferencesString = 'Response from Learner Inferences service: ' + response.text
            returnString += learnerInferencesString
            break
        if i == NUM_LEARNER_PATCH_RETRIES - 1:
            learnerInferencesString = ('Failed to update mastery estimates for learner {} ' + \
                'after {} tries').format(learnerTraitData['identifier'], NUM_LEARNER_PATCH_RETRIES)
            returnString += learnerInferencesString


    ''' POST xAPI statements to LRS '''
    global selfReportId
    if selfReportId is None:
        selfReportId = getSelfReportActivityId()

    learnerName = getLearnerName(learnerTraitData['identifier'])

    # Activity given ratings
    actorObject = {
        'objectType': 'Agent',
        'name': 'Recommender UI Support Service',
        'account': {
            'homePage': Config.BASE_URL,
            'name': 'Recommender UI Support Service'
        }
    }
    verbObject = {
        'id': 'http://id.tincanapi.com/verb/rated',
        'display': {
            'en-US': 'rated'
        }
    }
    objectObject = {
        'id': activityId
    }

    # Activity given popularity rating
    starRatingResultObject = {
        'score': {
            'raw': activityResponseDict['popularityRating'],
            'min': 1,
            'max': 5
        },
        'success': updateSuccess
    }
    starRatingStatement = {
        'actor': actorObject,
        'verb': verbObject,
        'object': objectObject,
        'result': starRatingResultObject
    }

    # Activity given emotion rating
    emotionRatingResultObject = {
        'success': updateSuccess,
        'response': activityResponseDict['emotionRating']
    }
    emotionRatingStatement = {
        'actor': actorObject,
        'verb': verbObject,
        'object': objectObject,
        'result': emotionRatingResultObject
    }

    # Learner completed self-report activity
    actorObject = {
        'objectType': 'Agent',
        'name': learnerName,
        'account': {
            'homePage': Config.KEYCLOAK_ENDPOINT,
            'name': activityResponseDict['learnerKeycloakId']
        }
    }
    verbObject = {
        'id': 'http://adlnet.gov/expapi/verbs/completed',
        'display': {
            'en-US': 'completed'
        }
    }
    objectObject = {
        'id': selfReportId
    }
    completedStatement = {
        'actor': actorObject,
        'verb': verbObject,
        'object': objectObject
    }

    # POST xAPI statements to LRS
    url = LRSConfig.HOST + ':' + LRSConfig.PORT + '/' + LRSConfig.ENDPOINT
    headers = {
        'X-Experience-API-Version': '1.0.0'
    }
    username = LRSConfig.USERNAME
    password = LRSConfig.PASSWORD
    requests.post(url, auth = HTTPBasicAuth(username, password), \
        json = starRatingStatement, headers = headers)
    requests.post(url, auth = HTTPBasicAuth(username, password), \
        json = emotionRatingStatement, headers = headers)
    requests.post(url, auth = HTTPBasicAuth(username, password), \
        json = completedStatement, headers = headers)
        
    return returnString
