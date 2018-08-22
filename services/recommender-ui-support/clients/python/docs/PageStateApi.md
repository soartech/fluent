# recommenderuisupportclient.PageStateApi

All URIs are relative to *https://fluent.tla/rui-support*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_page_state**](PageStateApi.md#delete_page_state) | **DELETE** /page-state/{keycloakId} | Deletes the page state for a user session
[**get_page_state**](PageStateApi.md#get_page_state) | **GET** /page-state/{keycloakId} | Obtains the page state for a user session
[**post_page_state**](PageStateApi.md#post_page_state) | **POST** /page-state | Stores the page state for a new user session
[**update_page_state**](PageStateApi.md#update_page_state) | **PATCH** /page-state/{keycloakId} | Updates the page state for a user session


# **delete_page_state**
> delete_page_state(keycloak_id)

Deletes the page state for a user session

Removes the page state for the given user session from the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.PageStateApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose page state will be deleted

try:
    # Deletes the page state for a user session
    api_instance.delete_page_state(keycloak_id)
except ApiException as e:
    print("Exception when calling PageStateApi->delete_page_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose page state will be deleted | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_page_state**
> PageState get_page_state(keycloak_id)

Obtains the page state for a user session

Obtains the page state for the given user session

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.PageStateApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose page state will be returned

try:
    # Obtains the page state for a user session
    api_response = api_instance.get_page_state(keycloak_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PageStateApi->get_page_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose page state will be returned | 

### Return type

[**PageState**](PageState.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_page_state**
> post_page_state(page_state_obj)

Stores the page state for a new user session

Stores the page state for a new user session in the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.PageStateApi()
page_state_obj = recommenderuisupportclient.PageState() # PageState | PageState object to add

try:
    # Stores the page state for a new user session
    api_instance.post_page_state(page_state_obj)
except ApiException as e:
    print("Exception when calling PageStateApi->post_page_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_state_obj** | [**PageState**](PageState.md)| PageState object to add | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_page_state**
> update_page_state(keycloak_id, page_state_obj)

Updates the page state for a user session

Updates the page state for the given user session in the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.PageStateApi()
keycloak_id = 'keycloak_id_example' # str | The ID of the learner whose page state will be updated
page_state_obj = recommenderuisupportclient.PageState() # PageState | PageState object to update

try:
    # Updates the page state for a user session
    api_instance.update_page_state(keycloak_id, page_state_obj)
except ApiException as e:
    print("Exception when calling PageStateApi->update_page_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keycloak_id** | **str**| The ID of the learner whose page state will be updated | 
 **page_state_obj** | [**PageState**](PageState.md)| PageState object to update | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

