# recommenderuisupportclient.ActivityResponsesApi

All URIs are relative to *https://fluent.tla/rui-support*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_activity_response**](ActivityResponsesApi.md#delete_activity_response) | **DELETE** /activity-responses/{activityId} | Deletes an activity and all its responses
[**post_activity_response**](ActivityResponsesApi.md#post_activity_response) | **POST** /activity-responses | Stores an activity self-report response


# **delete_activity_response**
> delete_activity_response(activity_id)

Deletes an activity and all its responses

Removes the activity and all responses associated with it from the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.ActivityResponsesApi()
activity_id = 'activity_id_example' # str | The ID of the activity to delete

try:
    # Deletes an activity and all its responses
    api_instance.delete_activity_response(activity_id)
except ApiException as e:
    print("Exception when calling ActivityResponsesApi->delete_activity_response: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_id** | **str**| The ID of the activity to delete | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_activity_response**
> post_activity_response(activity_response_obj)

Stores an activity self-report response

Adds a new activity response to the database; if this is the first activity response for the activity, also adds the activity to the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.ActivityResponsesApi()
activity_response_obj = recommenderuisupportclient.ActivityResponse() # ActivityResponse | ActivityResponse object to add

try:
    # Stores an activity self-report response
    api_instance.post_activity_response(activity_response_obj)
except ApiException as e:
    print("Exception when calling ActivityResponsesApi->post_activity_response: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_response_obj** | [**ActivityResponse**](ActivityResponse.md)| ActivityResponse object to add | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

