import requests
import json
import time
from requests.auth import HTTPBasicAuth
import datetime
from config import LRSConfig, LearnerInferenceConfig

def print_with_time(msg):
    time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    print("[{}] - {}".format(str(time), msg), flush=True)


with open('xapi_statements_fluent.json', 'r') as infile:
    xapi_statements = json.load(infile)

# If you want to test this, you have to hard code your LRS Client Credentials here.
usr = LRSConfig.USR
pwd = LRSConfig.PWD

url = "/".join([LRSConfig.HOST+":"+LRSConfig.PORT, LRSConfig.ENDPOINT])

headers = {
    'X-Experience-API-Version': '1.0.0'
}

try:
    with open('actor_mappings.json', 'r') as infile:
        actor_mappings = json.load(infile)
        for actor, id in actor_mappings.items():
            learner_url = "/".join([LearnerInferenceConfig.HOST+":"+LearnerInferenceConfig.PORT, LearnerInferenceConfig.ENDPOINT, id])
            r = requests.delete(learner_url)
            print_with_time(str(r.json()))
except FileNotFoundError:
    print('No prior mappings')

for statement in xapi_statements:
    print(statement['actor'])
actor_names = set([
    statement['actor']['name'] for statement in xapi_statements
])

actor_dict = {}

for actor in actor_names:
    # Create an actor object
    actor_object = {
        "email": "{}@example.com".format(actor),
        "gender": "Male",
        "name": actor,
        "@context": "string",
        "@type": "string",
        "masteryEstimates": [],
        "masteryProbabilities": [],
        "competencyAttemptCounters": [],
        'identifier': 'http://example.com'
    }

    # create the actor
    learner_post_url = "/".join([LearnerInferenceConfig.HOST+":"+LearnerInferenceConfig.PORT, LearnerInferenceConfig.ENDPOINT])
    r = requests.post(learner_post_url, json=actor_object)
    print(r.json())
    actor_db_id = r.json().get('id', None)
    actor_dict[actor] = actor_db_id

with open('actor_mappings.json', 'w') as outfile:
    json.dump(actor_dict, outfile)

# post each statement with 2 seconds in between
for statement in xapi_statements:
    if statement.get('result', None) is not None:
        if statement['result'].get('success', None) is not None:
            statement['actor']['name'] = actor_dict[statement['actor']['name']]
            statement['actor']['account']['name'] = actor_dict[statement['actor']['account']['name']]
            print_with_time('Sending statement')
            response = requests.post(url, auth=HTTPBasicAuth(usr, pwd), json=[statement], headers=headers)
            print_with_time(str(response.json()))
            time.sleep(2)
