# activity_index_client.AssociationsApi

All URIs are relative to *https://fluent.tla/activity-index*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_associations**](AssociationsApi.md#generate_associations) | **POST** /associations | Generates mapping from TLOs/ELOs to activities and token types to activities
[**get_competency_associations**](AssociationsApi.md#get_competency_associations) | **GET** /competency-associations | Obtains mapping of TLOs/ELOs to activities
[**get_token_associations**](AssociationsApi.md#get_token_associations) | **GET** /token-associations | Obtains mapping of token types to activities


# **generate_associations**
> generate_associations()

Generates mapping from TLOs/ELOs to activities and token types to activities

Generates a list of all activities mapped to their corresponding TLOs/ELOs and a list of all activities mapped to their corresponding token types

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.AssociationsApi()

try:
    # Generates mapping from TLOs/ELOs to activities and token types to activities
    api_instance.generate_associations()
except ApiException as e:
    print("Exception when calling AssociationsApi->generate_associations: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_competency_associations**
> list[CompetencyAssociations] get_competency_associations()

Obtains mapping of TLOs/ELOs to activities

Obtains the list of all activities mapped to their corresponding TLOs/ELOs

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.AssociationsApi()

try:
    # Obtains mapping of TLOs/ELOs to activities
    api_response = api_instance.get_competency_associations()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssociationsApi->get_competency_associations: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CompetencyAssociations]**](CompetencyAssociations.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_token_associations**
> list[TokenAssociations] get_token_associations()

Obtains mapping of token types to activities

Obtains the list of all activities mapped to their corresponding token types

### Example
```python
from __future__ import print_function
import time
import activity_index_client
from activity_index_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = activity_index_client.AssociationsApi()

try:
    # Obtains mapping of token types to activities
    api_response = api_instance.get_token_associations()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssociationsApi->get_token_associations: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[TokenAssociations]**](TokenAssociations.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

