import connexion
import six

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from activity_index_server.models.error import Error  # noqa: E501
from activity_index_server.models.learning_activity import LearningActivity  # noqa: E501
from activity_index_server import util
from activity_index_server.config import Config

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]


def get_activities(limit=None, offset=None):  # noqa: E501
    """Obtains multiple LearningActivity objects

    Returns a collection of LearningActivity objects; all activities are returned if \&quot;limit\&quot; and \&quot;offset\&quot; were not specified # noqa: E501

    :param limit: The maximum number of objects that will be returned
    :type limit: int
    :param offset: Determines the first object to be returned
    :type offset: int

    :rtype: List[LearningActivity]
    """
    
    if limit is None:
        limit = 0
    if offset is None:
        offset = 0

    activityDictList = []

    for activityDict in db.learning_activities.find({}, {'_id': 0}).limit(limit).skip(offset):
        # Obtain author document from author ObjectId
        if 'authorId' in activityDict and activityDict['authorId'] != None:
            authorId = activityDict['authorId']
            activityDict.pop('authorId')
            activityDict['author'] = db.authors.find_one({'_id': ObjectId(authorId)}, {'_id': 0})

        # Obtain publisher document from publisher ObjectId
        if 'publisherId' in activityDict and activityDict['publisherId'] != None:
            publisherId = activityDict['publisherId']
            activityDict.pop('publisherId')
            activityDict['publisher'] = db.publishers.find_one({'_id': ObjectId(publisherId)}, {'_id': 0})

        # Obtain provider document from provider ObjectId
        if 'providerId' in activityDict and activityDict['providerId'] != None:
            providerId = activityDict['providerId']
            activityDict.pop('providerId')
            activityDict['provider'] = db.providers.find_one({'_id': ObjectId(providerId)}, {'_id': 0})

        activityDictList.append(activityDict)
    
    return activityDictList

