import learner_inferences_client
from learner_inferences_client.rest import ApiException

api = learner_inferences_client.MultipleLearnersApi()
api.api_client.configuration.host = "insertIPAddr/learner-inferences"

try:
    response = api.get_learners()
    print(response)
except  ApiException as e:
    print("Exception when calling MultiplerLearnersApi->get_learners: %s\n" % e)
