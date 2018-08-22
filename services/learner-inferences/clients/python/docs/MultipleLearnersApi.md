# learner_inferences_client.MultipleLearnersApi

All URIs are relative to *https://fluent.tla/learner-inferences*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_learners**](MultipleLearnersApi.md#get_learners) | **GET** /learners | Obtains a collection of Learner objects from Learner Profile.


# **get_learners**
> list[Learner] get_learners(limit=limit, offset=offset)

Obtains a collection of Learner objects from Learner Profile.

Returns a collection of Learner objects; all learners are returned if \"limit\" and \"offset\" were not specified.

### Example
```python
from __future__ import print_function
import time
import learner_inferences_client
from learner_inferences_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = learner_inferences_client.MultipleLearnersApi()
limit = 56 # int | The maximum number of objects that will be returned. (optional)
offset = 56 # int | Determines the first object to be returned. (optional)

try:
    # Obtains a collection of Learner objects from Learner Profile.
    api_response = api_instance.get_learners(limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MultipleLearnersApi->get_learners: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| The maximum number of objects that will be returned. | [optional] 
 **offset** | **int**| Determines the first object to be returned. | [optional] 

### Return type

[**list[Learner]**](Learner.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

