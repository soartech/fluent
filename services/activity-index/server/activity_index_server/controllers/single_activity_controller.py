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
from activity_index_server.service_utils import ServiceJSONEncoder

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]


def recursivelyReplaceStringsInDict(d: dict) -> dict:
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = recursivelyReplaceStringsInList(value)
        elif isinstance(value, dict):
            d[key] = recursivelyReplaceStringsInDict(value)
        elif isinstance(value, str):
            d[key] = replaceTemplateValues(value)
    return d


def recursivelyReplaceStringsInList(lst: list) -> list:
    for i in range(len(lst)):
        if isinstance(lst[i], list):
            lst[i] = recursivelyReplaceStringsInList(lst[i])
        elif isinstance(lst[i], dict):
            lst[i] = recursivelyReplaceStringsInDict(lst[i])
        elif isinstance(lst[i], str):
            lst[i] = replaceTemplateValues(lst[i])
    return lst


def replaceTemplateValues(s: str) -> str:
    replacementsDict = {
        '{assessment-activity-provider-url}': Config.ASSESSMENT_ACTIVITY_PROVIDER_URL,
        '{video-player-url}': Config.VIDEO_PLAYER_URL,
        '{static-content-viewer-url}': Config.STATIC_CONTENT_VIEWER_URL,
        '{content-url}': Config.CONTENT_URL,
        '{contentBase}': Config.CONTENT_BASE,
        '{contentPort}': Config.CONTENT_PORT,
        '{moodle-url}': Config.MOODLE_URL
    }

    for key, value in replacementsDict.items():
        s = s.replace(key, value)
    return s


def separateAuthorPublisherProviderFromActivity(activityDict):
    returnString = ''
    
    if 'author' in activityDict and activityDict['author'] is not None:
        authorId = ''

        # Find the author of the current activity if it exists
        author = None
        if 'name' in activityDict['author'] and activityDict['author']['name'] is not None:
            author = db.authors.find_one({'name': activityDict['author']['name']}, {'_id': 1})

        author_endpoint = Config.AUTHOR_ENDPOINT
        if not author_endpoint.endswith("/"):
            author_endpoint += "/"
        
        if author is None:
            # Create a new author if necessary...
            authorId = str(db.authors.insert_one(activityDict['author']).inserted_id)
            db.authors.update({'_id': ObjectId(authorId)}, \
                {'$set': {'identifier': author_endpoint + authorId}})
            returnString += 'New author created with ID ' + authorId + '  '
        else:
            # ...otherwise, replace the author's info
            authorId = str(author['_id'])
            activityDict['author']['identifier'] = author_endpoint + authorId
            db.authors.update({'_id': ObjectId(authorId)}, activityDict['author'])
            returnString += 'Author with ID ' + authorId + ' updated  '

        # Remove the entire author object from the LearningActivity,
        # and just keep a reference to the author's ID
        activityDict.pop('author')
        activityDict['authorId'] = authorId

    if 'publisher' in activityDict and activityDict['publisher'] is not None:
        publisherId = ''
        
        # Find the publisher of the current activity if it exists
        publisher = None
        if 'url' in activityDict['publisher'] and activityDict['publisher']['url'] is not None:
            publisher = db.publishers.find_one({'url': activityDict['publisher']['url']}, {'_id': 1})

        publisher_endpoint = Config.PUBLISHER_ENDPOINT
        if not publisher_endpoint.endswith("/"):
            publisher_endpoint += "/"

        if publisher is None:
            # Create a new publisher if necessary...
            publisherId = str(db.publishers.insert_one(activityDict['publisher']).inserted_id)
            db.publishers.update({'_id': ObjectId(publisherId)}, \
                {'$set': {'identifier': publisher_endpoint + publisherId}})
            returnString += 'New publisher created with ID ' + publisherId + '  '
        else:
            # ...otherwise, replace the publisher's info
            publisherId = str(publisher['_id'])
            activityDict['publisher']['identifier'] = publisher_endpoint + publisherId
            db.publishers.update({'_id': ObjectId(publisherId)}, activityDict['publisher'])
            returnString += 'Publisher with ID ' + publisherId + ' updated  '
        
        # Remove the entire publisher object from the LearningActivity,
        # and just keep a reference to the publisher's ID
        activityDict.pop('publisher')
        activityDict['publisherId'] = publisherId

    if 'provider' in activityDict and activityDict['provider'] is not None:
        providerId = ''
        
        # Find the provider of the current activity if it exists
        provider = None
        if 'name' in activityDict['provider'] and activityDict['provider']['name'] is not None:
            provider = db.providers.find_one({'name': activityDict['provider']['name']}, {'_id': 1})

        provider_endpoint = Config.PROVIDER_ENDPOINT
        if not provider_endpoint.endswith("/"):
            provider_endpoint += "/"

        if provider is None:
            # Create a new provider if necessary...
            providerId = str(db.providers.insert_one(activityDict['provider']).inserted_id)
            db.providers.update({'_id': ObjectId(providerId)}, \
                {'$set': {'identifier': provider_endpoint + providerId}})
            returnString += 'New provider created with ID ' + providerId + '  '
        else:
            # ...otherwise, replace the provider's info
            providerId = str(provider['_id'])
            activityDict['provider']['identifier'] = provider_endpoint + providerId
            db.providers.update({'_id': ObjectId(providerId)}, activityDict['provider'])
            returnString += 'Provider with ID ' + providerId + ' updated  '

        # Remove the entire provider object from the LearningActivity,
        # and just keep a reference to the provider's ID
        activityDict.pop('provider')
        activityDict['providerId'] = providerId

    return activityDict, returnString


def delete_activity(activityId):  # noqa: E501
    """Deletes a LearningActivity object

    Removes the LearningActivity from the database # noqa: E501

    :param activityId: The ID of the requested LearningActivity
    :type activityId: str

    :rtype: None
    """
    
    dict = db.learning_activities.find_one({'_id': ObjectId(activityId)})
    if dict is not None:
        db.learning_activities.remove({'_id': ObjectId(activityId)})
        return 'Activity successfully removed'
    else:
        return 'Activity with ID ' + activityId + ' does not exist'


def get_activity(activityId):  # noqa: E501
    """Obtains LearningActivity info

    Obtains the information of the corresponding LearningActivity # noqa: E501

    :param activityId: The ID of the requested LearningActivity
    :type activityId: str

    :rtype: LearningActivity
    """
    
    activityDict = db.learning_activities.find_one({'_id': ObjectId(activityId)}, {'_id': 0})
    
    if activityDict is None:
        return 'Activity not found'
    
    # Obtain author document from author ObjectId
    if 'authorId' in activityDict and activityDict['authorId'] is not None:
        authorId = activityDict['authorId']
        activityDict.pop('authorId')
        activityDict['author'] = db.authors.find_one({'_id': ObjectId(authorId)}, {'_id': 0})

    # Obtain publisher document from publisher ObjectId
    if 'publisherId' in activityDict and activityDict['publisherId'] is not None:
        publisherId = activityDict['publisherId']
        activityDict.pop('publisherId')
        activityDict['publisher'] = db.publishers.find_one({'_id': ObjectId(publisherId)}, {'_id': 0})

    # Obtain provider document from provider ObjectId
    if 'providerId' in activityDict and activityDict['providerId'] is not None:
        providerId = activityDict['providerId']
        activityDict.pop('providerId')
        activityDict['provider'] = db.providers.find_one({'_id': ObjectId(providerId)}, {'_id': 0})

    return activityDict


def post_activity(activityObj):  # noqa: E501
    """Creates a LearningActivity

    Creates a new LearningActivity, which is given as a whole object in the payload # noqa: E501

    :param activityObj: LearningActivity object to add
    :type activityObj: dict | bytes

    :rtype: None
    """
    
    # Transform the JSON object into a LearningActivity class object
    # to fit the schema, and then turn that back into a dictionary
    activityObj = LearningActivity.from_dict(activityObj)  # noqa: E501
    activityDict = ServiceJSONEncoder(include_nulls=False).default(activityObj)

    if activityDict is None:
        return 'Error in converting json file to dictionary'
    
    removedFileInfo = ''
    # If a document created from the same metadataFile exists in the database, remove it
    if 'metadataFile' in activityDict and activityDict['metadataFile'] is not None:
        activityFromSameFile = db.learning_activities.find_one({'metadataFile': activityDict['metadataFile']}, {'_id': 1})
        if activityFromSameFile is not None:
            db.learning_activities.remove({'_id': activityFromSameFile['_id']})
            removedFileInfo = 'Activity created from file ' + activityDict['metadataFile'] + ' removed  '

    activityDict, returnString = separateAuthorPublisherProviderFromActivity(activityDict)
    activityDict = recursivelyReplaceStringsInDict(activityDict)
    returnString = removedFileInfo + returnString

    # Add the activity to the database
    activityId = str(db.learning_activities.insert_one(activityDict).inserted_id)
    
    # Update the fields requiring the activity's ID with the newly created ID
    activityDict['url'] = activityDict['url'].replace('{ActivityId}', activityId)
    db.learning_activities.update({'_id': ObjectId(activityId)}, \
        {'$set': {'identifier': activityId, 'url': activityDict['url']}})

    returnString += 'New activity created with ID ' + activityId
    return returnString


def update_activity(activityId, activityObj):  # noqa: E501
    """Updates LearningActivity info

    Updates the information of the LearningActivity, which is given partially (one or more of the top-level properties) in the payload # noqa: E501

    :param activityId: The ID of the requested LearningActivity
    :type activityId: str
    :param activityObj: LearningActivity object to update
    :type activityObj: dict | bytes

    :rtype: None
    """
    
    # IMPORTANT NOTE: this request may receive EITHER an activityId or metadataFile as a parameter
    
    activityObj2 = LearningActivity.from_dict(activityObj)
    activityDict = ServiceJSONEncoder(include_nulls=False).default(activityObj2)
    
    # If a metadata file name was given in place of the activityId, obtain the ID
    if activityId[-5:] == '.json':
        originFile = activityId
        tempDict = db.learning_activities.find_one({'metadataFile': originFile}, {'_id': 1})
        if tempDict is None:
            return post_activity(activityObj)
        activityId = str(tempDict['_id'])
    
    activity = db.learning_activities.find_one({'_id': ObjectId(activityId)}, {'_id': 1})
    if activity is None:
        return 'Activity not found'
    
    activityDict, returnString = separateAuthorPublisherProviderFromActivity(activityDict)
    activityDict = recursivelyReplaceStringsInDict(activityDict)

    # Update the fields requiring the activity's ID
    if 'identifier' in activityDict:
        activityDict['identifier'] = activityId
    if 'url' in activityDict and activityDict['url'] is not None:
        activityDict['url'] = activityDict['url'].replace('{ActivityId}', activityId)

    # Update the activity in the database
    db.learning_activities.update({'_id': ObjectId(activityId)}, {'$set': activityDict})
    return returnString + 'Activity updated successfully with ID ' + activityId

