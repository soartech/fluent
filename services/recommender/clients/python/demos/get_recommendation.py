from recommenderserver import config
import recommenderclient
from recommenderclient.rest import ApiException

api = recommenderclient.api.RecommendationApi()
api.api_client.configuration.host = config.Config.RECOMMENDER_URL

try:
    response = api.recommendation_get('dummyUserId')
    print(response)
except  ApiException as e:
    print("Exception when calling RecommenderApi->recommendation_get: %s\n" % e)
