import connexion
import six

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from swagger_server.models.ao_image import AoImage
from swagger_server.models.error import Error
from swagger_server import util
from swagger_server.config import Config
from swagger_server.encoder import JSONEncoder

client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
db = client[Config.MONGO_DB]


def get_ao_image():
    """
    Returns the AO Image stored by the database

    :rtype: AoImage
    """
    aoImageDict = db.ao_image.find_one({}, {'_id': 0})
    if aoImageDict is None:
        return 'AO Image has not been set yet'
    return aoImageDict


def post_ao_image(aoImageObj):
    """
    Stores the AO Image in the database

    :param aoImageObj: AoImage object to add
    :type aoImageObj: dict | bytes
    :rtype: None
    """
    aoImageObj = AoImage.from_dict(connexion.request.get_json())
    aoImageDict = JSONEncoder().default(aoImageObj)
    
    db.ao_image.remove({})
    db.ao_image.insert_one(aoImageDict)
    
    return 'AO Image was set'
