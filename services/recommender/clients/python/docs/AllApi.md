# recommenderclient.AllApi

All URIs are relative to *http://localhost/recommender*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all_get**](AllApi.md#all_get) | **GET** /all | Get all activities


# **all_get**
> Recommendation all_get(learner_id)

Get all activities

Returns all activities.

### Example
```python
from __future__ import print_function
import time
import recommenderclient
from recommenderclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderclient.AllApi()
learner_id = 'learner_id_example' # str | Id of the learner to get a recommendation for

try:
    # Get all activities
    api_response = api_instance.all_get(learner_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AllApi->all_get: %s\n" % e)
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

