# activity_index_client.SingleActivityApi

All URIs are relative to *https://fluent.tla/activity-index*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_activity**](SingleActivityApi.md#delete_activity) | **DELETE** /activities/{activityId} | Deletes a LearningActivity object
[**get_activity**](SingleActivityApi.md#get_activity) | **GET** /activities/{activityId} | Obtains LearningActivity info
[**post_activity**](SingleActivityApi.md#post_activity) | **POST** /activities | Creates a LearningActivity.
[**update_activity**](SingleActivityApi.md#update_activity) | **PATCH** /activities/{activityId} | Updates LearningActivity info


# **delete_activity**
> delete_activity(activity_id)

Deletes a LearningActivity object

Removes the LearningActivity from the database

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.SingleActivityApi()
activity_id = 'activity_id_example' # str | The ID of the requested LearningActivity

try:
    # Deletes a LearningActivity object
    api_instance.delete_activity(activity_id)
except ApiException as e:
    print("Exception when calling SingleActivityApi->delete_activity: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_id** | **str**| The ID of the requested LearningActivity | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_activity**
> LearningActivity get_activity(activity_id)

Obtains LearningActivity info

Obtains the information of the corresponding LearningActivity

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.SingleActivityApi()
activity_id = 'activity_id_example' # str | The ID of the requested LearningActivity

try:
    # Obtains LearningActivity info
    api_response = api_instance.get_activity(activity_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SingleActivityApi->get_activity: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_id** | **str**| The ID of the requested LearningActivity | 

### Return type

[**LearningActivity**](LearningActivity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_activity**
> post_activity(activity_obj)

Creates a LearningActivity.

Creates a new LearningActivity, which is given as a whole object in the payload.

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.SingleActivityApi()
activity_obj = activity_index_client.LearningActivity() # LearningActivity | LearningActivity object to add.

try:
    # Creates a LearningActivity.
    api_instance.post_activity(activity_obj)
except ApiException as e:
    print("Exception when calling SingleActivityApi->post_activity: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_obj** | [**LearningActivity**](LearningActivity.md)| LearningActivity object to add. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_activity**
> update_activity(activity_id, activity_obj)

Updates LearningActivity info

Updates the information of the LearningActivity, which is given partially (one or more of the top-level properties) in the payload

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.SingleActivityApi()
activity_id = 'activity_id_example' # str | The ID of the requested LearningActivity
activity_obj = NULL # object | LearningActivity object to update

try:
    # Updates LearningActivity info
    api_instance.update_activity(activity_id, activity_obj)
except ApiException as e:
    print("Exception when calling SingleActivityApi->update_activity: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_id** | **str**| The ID of the requested LearningActivity | 
 **activity_obj** | **object**| LearningActivity object to update | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

