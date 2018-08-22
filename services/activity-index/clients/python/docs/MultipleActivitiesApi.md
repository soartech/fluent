# activity_index_client.MultipleActivitiesApi

All URIs are relative to *https://fluent.tla/activity-index*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_activities**](MultipleActivitiesApi.md#get_activities) | **GET** /activities | Obtains multiple LearningActivity objects


# **get_activities**
> list[LearningActivity] get_activities(limit=limit, offset=offset)

Obtains multiple LearningActivity objects

Returns a collection of LearningActivity objects; all activities are returned if \"limit\" and \"offset\" were not specified

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.MultipleActivitiesApi()
limit = 56 # int | The maximum number of objects that will be returned (optional)
offset = 56 # int | Determines the first object to be returned (optional)

try:
    # Obtains multiple LearningActivity objects
    api_response = api_instance.get_activities(limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MultipleActivitiesApi->get_activities: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| The maximum number of objects that will be returned | [optional] 
 **offset** | **int**| Determines the first object to be returned | [optional] 

### Return type

[**list[LearningActivity]**](LearningActivity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

