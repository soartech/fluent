# recommenderuisupportclient.AOImageApi

All URIs are relative to *https://fluent.tla/rui-support*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_ao_image**](AOImageApi.md#get_ao_image) | **GET** /ao-image | Obtains the AO Image
[**post_ao_image**](AOImageApi.md#post_ao_image) | **POST** /ao-image | Stores the AO Image


# **get_ao_image**
> AoImage get_ao_image()

Obtains the AO Image

Returns the AO Image stored by the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.AOImageApi()

try:
    # Obtains the AO Image
    api_response = api_instance.get_ao_image()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AOImageApi->get_ao_image: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AoImage**](AoImage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_ao_image**
> post_ao_image(ao_image_obj)

Stores the AO Image

Stores the AO Image in the database

### Example
```python
from __future__ import print_function
import time
import recommenderuisupportclient
from recommenderuisupportclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = recommenderuisupportclient.AOImageApi()
ao_image_obj = recommenderuisupportclient.AoImage() # AoImage | AoImage object to add

try:
    # Stores the AO Image
    api_instance.post_ao_image(ao_image_obj)
except ApiException as e:
    print("Exception when calling AOImageApi->post_ao_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ao_image_obj** | [**AoImage**](AoImage.md)| AoImage object to add | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

