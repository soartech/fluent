# recommenderuisupportclient.TokensApi

All URIs are relative to *https://fluent.tla/rui-support*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_learner_tokens**](TokensApi.md#delete_learner_tokens) | **DELETE** /tokens/{keycloakId} | Deletes a learner&#39;s tokens
[**get_learner_tokens**](TokensApi.md#get_learner_tokens) | **GET** /tokens/{keycloakId} | Obtains the tokens for a learner
[**post_learner_tokens**](TokensApi.md#post_learner_tokens) | **POST** /tokens | Adds a new learner to the database with no tokens
[**update_learner_tokens**](TokensApi.md#update_learner_tokens) | **PATCH** /tokens/{keycloakId} | Updates a learner&#39;s tokens


# **delete_learner_tokens**
> delete_learner_tokens(keycloak_id)

Deletes a learner's tokens

Removes the learner from the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.TokensApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner to delete

try:
    # Deletes a learner's tokens
    api_instance.delete_learner_tokens(keycloak_id)
except ApiException as e:
    print("Exception when calling TokensApi->delete_learner_tokens: %s\n" % e)
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

# **get_learner_tokens**
> LearnerTokens get_learner_tokens(keycloak_id)

Obtains the tokens for a learner

Returns the set of tokens the learner has earned so far

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.TokensApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose tokens will be returned

try:
    # Obtains the tokens for a learner
    api_response = api_instance.get_learner_tokens(keycloak_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->get_learner_tokens: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose tokens will be returned | 

### Return type

[**LearnerTokens**](LearnerTokens.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_learner_tokens**
> post_learner_tokens(learner_tokens_obj)

Adds a new learner to the database with no tokens

Adds a new learner to the database with an empty set of tokens

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.TokensApi()
learner_tokens_obj = recommenderuisupportclient.LearnerTokens() # LearnerTokens | LearnerTokens object to add

try:
    # Adds a new learner to the database with no tokens
    api_instance.post_learner_tokens(learner_tokens_obj)
except ApiException as e:
    print("Exception when calling TokensApi->post_learner_tokens: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **learner_tokens_obj** | [**LearnerTokens**](LearnerTokens.md)| LearnerTokens object to add | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_learner_tokens**
> update_learner_tokens(keycloak_id, learner_tokens_obj)

Updates a learner's tokens

Adds some tokens to the learner's current set of tokens

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.TokensApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose tokens will be updated
learner_tokens_obj = recommenderuisupportclient.LearnerTokens() # LearnerTokens | LearnerTokens object to update

try:
    # Updates a learner's tokens
    api_instance.update_learner_tokens(keycloak_id, learner_tokens_obj)
except ApiException as e:
    print("Exception when calling TokensApi->update_learner_tokens: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose tokens will be updated | 
 **learner_tokens_obj** | [**LearnerTokens**](LearnerTokens.md)| LearnerTokens object to update | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

