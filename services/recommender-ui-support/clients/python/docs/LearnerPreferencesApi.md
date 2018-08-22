# recommenderuisupportclient.LearnerPreferencesApi

All URIs are relative to *https://fluent.tla/rui-support*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_learner_preferences**](LearnerPreferencesApi.md#delete_learner_preferences) | **DELETE** /learner-preferences/{keycloakId} | Deletes a learner&#39;s preferences
[**post_learner_preferences**](LearnerPreferencesApi.md#post_learner_preferences) | **POST** /learner-preferences/{keycloakId} | Stores a learner&#39;s preferences
[**update_learner_preferences**](LearnerPreferencesApi.md#update_learner_preferences) | **PATCH** /learner-preferences/{keycloakId} | Updates a learner&#39;s preferences


# **delete_learner_preferences**
> delete_learner_preferences(keycloak_id)

Deletes a learner's preferences

Removes the learner from the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.LearnerPreferencesApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner to delete

try:
    # Deletes a learner's preferences
    api_instance.delete_learner_preferences(keycloak_id)
except ApiException as e:
    print("Exception when calling LearnerPreferencesApi->delete_learner_preferences: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner to delete | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_learner_preferences**
> post_learner_preferences(keycloak_id, learner_preferences_obj)

Stores a learner's preferences

Adds a new learner to the database along with their initial preferences

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.LearnerPreferencesApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose preferences will be added
learner_preferences_obj = recommenderuisupportclient.LearnerPreferences() # LearnerPreferences | LearnerPreferences object to add

try:
    # Stores a learner's preferences
    api_instance.post_learner_preferences(keycloak_id, learner_preferences_obj)
except ApiException as e:
    print("Exception when calling LearnerPreferencesApi->post_learner_preferences: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose preferences will be added | 
 **learner_preferences_obj** | [**LearnerPreferences**](LearnerPreferences.md)| LearnerPreferences object to add | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_learner_preferences**
> update_learner_preferences(keycloak_id, learner_preferences_obj)

Updates a learner's preferences

Updates the learner's preferences in the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.LearnerPreferencesApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose preferences will be updated
learner_preferences_obj = recommenderuisupportclient.LearnerPreferences() # LearnerPreferences | LearnerPreferences object to update

try:
    # Updates a learner's preferences
    api_instance.update_learner_preferences(keycloak_id, learner_preferences_obj)
except ApiException as e:
    print("Exception when calling LearnerPreferencesApi->update_learner_preferences: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose preferences will be updated | 
 **learner_preferences_obj** | [**LearnerPreferences**](LearnerPreferences.md)| LearnerPreferences object to update | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

