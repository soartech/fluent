# recommenderclient.UpcomingApi

All URIs are relative to *http://localhost/recommender*

Method | HTTP request | Description
------------- | ------------- | -------------
[**upcoming_get**](UpcomingApi.md#upcoming_get) | **GET** /upcoming | Get upcoming activities


# **upcoming_get**
> Recommendation upcoming_get(learner_id)

Get upcoming activities

Returns an overview of what the learner will be working on (and reflected in upcoming recommendations). It should include current ELO in the sequence that the learner has not yet mastered that they will continue learning. It will also include any ELOs that the learner has forgotten that will be reviewed.

### Example
```python
from __future__ import print_function
import time
import recommenderclient
from recommenderclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderclient.UpcomingApi()
learner_id = 'learner_id_example' # str | Id of the learner to get a recommendation for

try:
    # Get upcoming activities
    api_response = api_instance.upcoming_get(learner_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UpcomingApi->upcoming_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **learner_id** | **str**| Id of the learner to get a recommendation for | 

### Return type

[**Recommendation**](Recommendation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

