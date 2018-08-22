import connexion
import six

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from activity_index_server.models.competency_associations import CompetencyAssociations  # noqa: E501
from activity_index_server.models.error import Error  # noqa: E501
from activity_index_server.models.token_associations import TokenAssociations  # noqa: E501
from activity_index_server import util
from activity_index_server.config import Config
from cass_client.models import Competency
from cass_graph_client.cass_graph import CassGraph
from recommenderserver.recommender.utils import load_or_instantiate

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]


def generate_associations():  # noqa: E501
    """Generates mapping from TLOs/ELOs to activities and token types to activities

    Generates a list of all activities mapped to their corresponding TLOs/ELOs and a list of all activities mapped to their corresponding token types # noqa: E501


    :rtype: None
    """

    db.activity_associations.remove({})
    db.token_associations.remove({})
    activityCursor = db.learning_activities.find({})
    cass_graph = load_or_instantiate('recommenderserver.resources', CassGraph, '59e884bb-510b-4f36-8443-8c3842336e28')
    
    # Generate activity associations
    while 0 == 0:
        try:
            activityDict = activityCursor.next()
        except StopIteration:
            break
        if 'educationalAlignment' in activityDict:
            for alignment in activityDict['educationalAlignment']:
                if 'additionalType' in alignment and (alignment['additionalType'] == 'TLOAlignment' \
                    or alignment['additionalType'] == 'ELOAlignment'):
                    db.activity_associations.update({'competency': alignment['targetUrl']}, \
                        {'$addToSet': {'activities': str(activityDict['_id'])}}, upsert = True)

    # Generate token associations
    activityAssociationsCursor = db.activity_associations.find({}, {'_id': 0})
    while 0 == 0:
        try:
            activityAssociationsDict = activityAssociationsCursor.next()
        except StopIteration:
            break
        if activityAssociationsDict['competency'] in cass_graph.competency_objs:
            competencyNode = cass_graph.competency_objs[activityAssociationsDict['competency']]
            if competencyNode is not None and competencyNode.ceasncoded_notation is not None:
                tokenType = competencyNode.ceasncoded_notation
                if '.' in competencyNode.ceasncoded_notation:
                    tokenType = competencyNode.ceasncoded_notation[:competencyNode.ceasncoded_notation.rfind('.')]
                for activity in activityAssociationsDict['activities']:
                    db.token_associations.update({'tokenType': tokenType}, \
                        {'$addToSet': {'activities': activity}}, upsert = True)

    return 'Activity associations generated'


def get_competency_associations():  # noqa: E501
    """Obtains mapping of TLOs/ELOs to activities

    Obtains the list of all activities mapped to their corresponding TLOs/ELOs # noqa: E501


    :rtype: List[CompetencyAssociations]
    """

    activityAssociationsArray = []
    activityAssociationsCursor = db.activity_associations.find({}, {'_id': 0})
    
    while 0 == 0:
        try:
            activityAssociationsDict = activityAssociationsCursor.next()
        except StopIteration:
            break
        activityAssociationsArray.append(activityAssociationsDict)
    
    return activityAssociationsArray


def get_token_associations():  # noqa: E501
    """Obtains mapping of token types to activities

    Obtains the list of all activities mapped to their corresponding token types # noqa: E501


    :rtype: List[TokenAssociations]
    """

    tokenAssociationsArray = []
    tokenAssociationsCursor = db.token_associations.find({}, {'_id': 0})

    while 0 == 0:
        try:
            tokenAssociationsDict = tokenAssociationsCursor.next()
        except StopIteration:
            break
        tokenAssociationsArray.append(tokenAssociationsDict)

    return tokenAssociationsArray

