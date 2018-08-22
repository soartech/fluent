import connexion
import six

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from swagger_server.models.error import Error
from swagger_server.models.learner_tokens import LearnerTokens
from swagger_server import util
from swagger_server.config import Config
from swagger_server.service_utils import ServiceJSONEncoder

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]


def delete_learner_tokens(keycloakId):
    """
    Removes the learner from the database

    :param keycloakId: The ID of the learner to delete
    :type keycloakId: str
    :rtype: None
    """
    
    learnerTokensDict = db.learner_tokens.find_one({'learnerKeycloakId': keycloakId})
    if learnerTokensDict is None:
        return 'Learner tokens for learner with ID ' + keycloakId + ' do not exist'
    db.learner_tokens.remove({'learnerKeycloakId': keycloakId})
    return 'Learner tokens successfully removed'


def get_learner_tokens(keycloakId):
    """
    Returns the set of tokens the learner has earned so far

    :param keycloakId: The ID of the learner whose tokens will be returned
    :type keycloakId: str
    :rtype: LearnerTokens
    """

    learnerTokensDict = db.learner_tokens.find_one({'learnerKeycloakId': keycloakId}, {'_id': 0})
    if learnerTokensDict is None:
        return 'Learner tokens for learner with ID ' + keycloakId + ' do not exist'
    return learnerTokensDict


def post_learner_tokens(learnerTokensObj):
    """
    Adds a new learner to the database with an empty set of tokens

    :param learnerTokensObj: LearnerTokens object to add
    :type learnerTokensObj: dict | bytes
    :rtype: None
    """
    
    learnerTokensObj = LearnerTokens.from_dict(connexion.request.get_json())
    learnerTokensDict = ServiceJSONEncoder().default(learnerTokensObj)
    
    existingLearnerTokensDict = db.learner_tokens.find_one({'learnerKeycloakId': \
        learnerTokensDict['learnerKeycloakId']}, {'_id': 0})
    if existingLearnerTokensDict is not None:
        return 'Learner tokens for learner with ID ' + learnerTokensDict['learnerKeycloakId'] + ' already exist'

    db.learner_tokens.insert_one(learnerTokensDict)
    
    return 'New tokens created for learner with ID ' + learnerTokensDict['learnerKeycloakId']


def update_learner_tokens(keycloakId, learnerTokensObj):
    """
    Adds some tokens to the learner's current set of tokens

    :param keycloakId: The ID of the learner whose tokens will be updated
    :type keycloakId: str
    :param learnerTokensObj: LearnerTokens object to update
    :type learnerTokensObj: dict | bytes
    :rtype: None
    """
    
    existingLearnerTokensDict = db.learner_tokens.find_one({'learnerKeycloakId': keycloakId}, {'_id': 0})
    if existingLearnerTokensDict is None:
        return 'Learner tokens for learner with ID ' + keycloakId + ' do not exist'
    
    learnerTokensObj = LearnerTokens.from_dict(connexion.request.get_json())
    learnerTokensDict = ServiceJSONEncoder().default(learnerTokensObj)

    # Add tokens
    if 'tokens' in learnerTokensDict:
        numModified = 0
        if len(learnerTokensDict['tokens']) == 0 or 'type' not in learnerTokensDict['tokens'][0] or \
            'count' not in learnerTokensDict['tokens'][0]:
            return 'Error: invalid tokens array provided'
        if 'tokens' in existingLearnerTokensDict:
            # Look for tokens of the requested type and increment their count by the given amount if they exist...
            numModified = db.learner_tokens.update({'learnerKeycloakId': keycloakId, 'tokens.type': \
                learnerTokensDict['tokens'][0]['type']}, {'$inc': \
                {'tokens.$.count': learnerTokensDict['tokens'][0]['count']}})['nModified']
        if numModified == 0 and learnerTokensDict['tokens'][0]['count'] != 0:
            # ... or create them if they don't exist
            db.learner_tokens.update({'learnerKeycloakId': keycloakId}, \
                {'$push': {'tokens': learnerTokensDict['tokens'][0]}})
        return 'Tokens given to learner with ID ' + keycloakId

    return 'Error: no tokens in JSON object'
