import collections
import json
import pickle
from os import path
from typing import Dict, Tuple, List

from activity_index_client import LearningActivity
from activity_index_client.api_client import ApiClient as ActivityApiClient
from cass_graph_client.cass_graph import CassGraph
from learner_inferences_client import Learner
from learner_inferences_client.api_client import ApiClient as LearnerApiClient
from recommenderserver.recommender.utils import mongo_id_from_url
from recommenderuisupportclient.models import LearnerTokens
from recommenderuisupportclient.api_client import ApiClient as RecommenderUIApiClient

resources_dir = path.join(path.dirname(__file__), 'resources')
cass_graph_pickle_file = path.join(resources_dir, 'cass_graph.pkl')
learners_json_file = path.join(resources_dir, 'learners.json')
activities_json_file = path.join(resources_dir, 'activities.json')
learner_tokens_json_file = path.join(resources_dir, 'tokens.json')

FakeHttpResponse = collections.namedtuple('FakeHttpResponse', 'data')


def load_test_learners() -> Tuple[Dict[str, Learner], Dict[str, Learner]]:
    with open(learners_json_file, "r") as f:
        learners = json.loads(f.read())

    name_to_learner = {}
    id_to_learner = {}

    for learner in learners:
        learner = FakeHttpResponse(data=json.dumps(learner))
        learner = LearnerApiClient().deserialize(response=learner, response_type=Learner)
        name_to_learner[learner.name] = learner
        id_to_learner[mongo_id_from_url(learner.identifier)] = learner

    return name_to_learner, id_to_learner


def load_test_activities() -> Tuple[Dict[str, LearningActivity], Dict[str, LearningActivity]]:
    with open(activities_json_file, "r") as f:
        activities = json.loads(f.read())

    name_to_activity = {}
    id_to_activity = {}

    for activity in activities:
        activity = FakeHttpResponse(data=json.dumps(activity))
        activity = ActivityApiClient().deserialize(response=activity, response_type=LearningActivity)
        name_to_activity[activity.name] = activity
        id_to_activity[mongo_id_from_url(activity.identifier)] = activity

    return name_to_activity, id_to_activity

def load_test_activities_all() -> List[LearningActivity]:
    with open(activities_json_file, "r") as f:
        activities = json.load(f)

    activity_list = list()
    for activity in activities:
        activity = FakeHttpResponse(data=json.dumps(activity))
        activity = ActivityApiClient().deserialize(response=activity, response_type=LearningActivity)
        activity_list.append(activity)

    return activity_list

def load_test_tokens() -> Dict[str, LearnerTokens]:
    with open(learner_tokens_json_file, "r") as f:
        tokens = json.loads(f.read())

    learner_tokens_dict = dict()
    for learner_tokens in tokens:
        learner_tokens = FakeHttpResponse(data=json.dumps(learner_tokens))
        learner_tokens = RecommenderUIApiClient().deserialize(response=learner_tokens, response_type=LearnerTokens)
        learner_tokens_dict[learner_tokens.learner_keycloak_id] = learner_tokens

    return learner_tokens_dict

def dump_cass_graph(cass_graph: CassGraph):
    file = open(cass_graph_pickle_file, 'wb')
    pickle.dump(cass_graph, file)
    file.close()

def load_cass_graph() -> CassGraph:

    file = open(cass_graph_pickle_file, 'rb')
    cass_graph = pickle.load(file)
    file.close()
    return cass_graph

def cass_pickle_exists() -> bool:
    return path.exists(cass_graph_pickle_file)
