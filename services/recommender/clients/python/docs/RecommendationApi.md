# recommenderclient.RecommendationApi

All URIs are relative to *http://localhost/recommender*

Method | HTTP request | Description
------------- | ------------- | -------------
[**recommendation_get**](RecommendationApi.md#recommendation_get) | **GET** /recommendation | Get a new recommendation


# **recommendation_get**
> Recommendation recommendation_get(learner_id, focused_competencies=focused_competencies)

Get a new recommendation



### Example
```python
from __future__ import print_function
import time
import recommenderclient
from recommenderclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderclient.RecommendationApi()
learner_id = 'learner_id_example' # str | Id of the learner to get a recommendation for
focused_competencies = true # bool | Optional parameter to toggle focused competencies (optional)

try:
    # Get a new recommendation
    api_response = api_instance.recommendation_get(learner_id, focused_competencies=focused_competencies)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RecommendationApi->recommendation_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **learner_id** | **str**| Id of the learner to get a recommendation for | 
 **focused_competencies** | **bool**| Optional parameter to toggle focused competencies | [optional] 

### Return type

[**Recommendation**](Recommendation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

