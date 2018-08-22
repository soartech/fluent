import connexion
import six
import requests

import pymongo
from pymongo import MongoClient
from pprint import pprint

import json
from bson import json_util, ObjectId

from swagger_server.models.error import Error
from swagger_server.models.learner_goals import LearnerGoals
from swagger_server import util
from swagger_server.config import Config
from swagger_server.encoder import JSONEncoder

NUM_LEARNER_PATCH_RETRIES = 10


def update_goals(keycloakId, learnerGoalsObj):
    """
    Allows the UI to update the goals of a learner while avoiding Learner Inference service concurrency issues

    :param keycloakId: The ID of the learner whose goals will be updated
    :type keycloakId: str
    :param learnerGoalsObj: New learner goals
    :type learnerGoalsObj: dict | bytes
    :rtype: None
    """
    
    learnerGoalsObj = LearnerGoals.from_dict(connexion.request.get_json())
    learnerGoalsDict = JSONEncoder().default(learnerGoalsObj)
    
    url = Config.LEARNER_INFERENCES_ENDPOINT + '/' + keycloakId

    # PATCH learner trait data to Learner Inferences service
    for i in range(NUM_LEARNER_PATCH_RETRIES):
        response = requests.get(url)
        etag = response.headers['ETag']
        headers = {'content-type': 'application/json', 'if-match': etag}
        response = requests.patch(url, data = json.dumps(learnerGoalsDict), headers = headers)
        if response.status_code == 200:
            return 'Response from Learner Inferences service: ' + response.text
        if i == NUM_LEARNER_PATCH_RETRIES - 1:
            return ('Failed to update goals for learner {} after ' + \
                '{} tries').format(keycloakId, NUM_LEARNER_PATCH_RETRIES)
    
    return "Congratulations! You've received an error that should never occur!"
