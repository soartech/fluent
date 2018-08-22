# learner_inferences_client.SingleLearnerApi

All URIs are relative to *https://fluent.tla/learner-inferences*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_learner**](SingleLearnerApi.md#delete_learner) | **DELETE** /learners/{keycloakId} | Deletes a Learner object.
[**get_learner**](SingleLearnerApi.md#get_learner) | **GET** /learners/{keycloakId} | Obtains Learner info.
[**post_learner**](SingleLearnerApi.md#post_learner) | **POST** /learners | Creates one Learner in Learner Profile.
[**update_learner**](SingleLearnerApi.md#update_learner) | **PATCH** /learners/{keycloakId} | Updates Learner info.


# **delete_learner**
> delete_learner(keycloak_id)

Deletes a Learner object.

Removes the Learner from the database.

### Example
```python
from __future__ import print_function
import time
import learner_inferences_client
from learner_inferences_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = learner_inferences_client.SingleLearnerApi()
keycloak_id = 'keycloak_id_example' # str | The Keycloak ID of the Learner to be deleted.

try:
    # Deletes a Learner object.
    api_instance.delete_learner(keycloak_id)
except ApiException as e:
    print("Exception when calling SingleLearnerApi->delete_learner: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The Keycloak ID of the Learner to be deleted. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_learner**
> Learner get_learner(keycloak_id)

Obtains Learner info.

Obtains the information of the corresponding Learner.

### Example
```python
from __future__ import print_function
import time
import learner_inferences_client
from learner_inferences_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = learner_inferences_client.SingleLearnerApi()
keycloak_id = 'keycloak_id_example' # str | The Keycloak ID of the requested Learner.

try:
    # Obtains Learner info.
    api_response = api_instance.get_learner(keycloak_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SingleLearnerApi->get_learner: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The Keycloak ID of the requested Learner. | 

### Return type

[**Learner**](Learner.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_learner**
> post_learner(learner_obj)

Creates one Learner in Learner Profile.

Creates a Learner, which is given as a whole object in the payload.

### Example
```python
from __future__ import print_function
import time
import learner_inferences_client
from learner_inferences_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = learner_inferences_client.SingleLearnerApi()
learner_obj = learner_inferences_client.Learner() # Learner | Learner object to add.

try:
    # Creates one Learner in Learner Profile.
    api_instance.post_learner(learner_obj)
except ApiException as e:
    print("Exception when calling SingleLearnerApi->post_learner: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **learner_obj** | [**Learner**](Learner.md)| Learner object to add. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_learner**
> update_learner(keycloak_id, if_match, learner_obj)

Updates Learner info.

Updates the information of the Learner, which is given partially (one or more of the top-level properties) in the payload.

### Example
```python
from __future__ import print_function
import time
import learner_inferences_client
from learner_inferences_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = learner_inferences_client.SingleLearnerApi()
keycloak_id = 'keycloak_id_example' # str | The Keycloak ID of the requested Learner.
if_match = 'if_match_example' # str | The ETag of the learner object when it was last fetched
learner_obj = NULL # object | Learner object to update.

try:
    # Updates Learner info.
    api_instance.update_learner(keycloak_id, if_match, learner_obj)
except ApiException as e:
    print("Exception when calling SingleLearnerApi->update_learner: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The Keycloak ID of the requested Learner. | 
 **if_match** | **str**| The ETag of the learner object when it was last fetched | 
 **learner_obj** | **object**| Learner object to update. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

