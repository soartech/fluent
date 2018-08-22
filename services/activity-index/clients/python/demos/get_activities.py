import activity_index_client
from activity_index_client.rest import ApiException
import server.activity_index_server.config as config

api = activity_index_client.MultipleActivitiesApi()
api.api_client.configuration.host = config.Config.BASE_URL

try:
    response = api.get_activities()
    print(response)
except  ApiException as e:
    print("Exception when calling MultipleActivitiesApi->get_activities: %s\n" % e)
