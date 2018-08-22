import connexion
import six

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from swagger_server.models.error import Error
from swagger_server.models.page_state import PageState
from swagger_server import util
from swagger_server.config import Config
from swagger_server.encoder import JSONEncoder

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]


def delete_page_state(keycloakId):
    """
    Removes the page state for the given user session from the database

    :param keycloakId: The ID of the page state to delete
    :type keycloakId: str
    :rtype: None
    """

    pageStateDict = db.page_states.find_one({'learnerKeycloakId': keycloakId})
    if pageStateDict is None:
        return 'Page state for user session with ID ' + keycloakId + ' does not exist'
    db.page_states.remove({'learnerKeycloakId': keycloakId})
    return 'Page state successfully removed'


def get_page_state(keycloakId):
    """
    Obtains the page state for the given user session

    :param keycloakId: The ID of the user session
    :type keycloakId: str
    :rtype: PageState
    """
    
    pageStateDict = db.page_states.find_one({'learnerKeycloakId': keycloakId}, {'_id': 0})
    if pageStateDict is None:
        return 'Page state for user session with ID ' + keycloakId + ' does not exist'
    return pageStateDict


def post_page_state(pageStateObj):
    """
    Stores the page state for a new user session in the database

    :param pageStateObj: PageState object to add
    :type pageStateObj: dict | bytes
    :rtype: None
    """
    
    pageStateObj = PageState.from_dict(connexion.request.get_json())
    pageStateDict = JSONEncoder().default(pageStateObj)
    
    existingPageStateDict = db.page_states.find_one({'learnerKeycloakId': \
        pageStateDict['learnerKeycloakId']}, {'_id': 0})
    if existingPageStateDict is not None:
        return 'Page state for user session with ID ' + pageStateDict['learnerKeycloakId'] + ' already exists'
    
    db.page_states.insert_one(pageStateDict)
    
    return 'New page state created for user session with ID ' + pageStateDict['learnerKeycloakId']


def update_page_state(keycloakId, pageStateObj):
    """
    Updates the page state for the given user session in the database

    :param keycloakId: The ID of the page state which will be updated
    :type keycloakId: str
    :param pageStateObj: PageState object to update
    :type pageStateObj: dict | bytes
    :rtype: None
    """
    
    pageStateDict = db.page_states.find_one({'learnerKeycloakId': keycloakId}, {'_id': 0})
    if pageStateDict is None:
        return 'Page state for user session with ID ' + keycloakId + ' does not exist'
    
    pageStateObj = PageState.from_dict(connexion.request.get_json())
    pageStateDict = JSONEncoder().default(pageStateObj)
    db.page_states.update({'learnerKeycloakId': keycloakId}, {'$set': pageStateDict})
    
    return 'Page state updated successfully for user session with ID ' + keycloakId
