# cass_client.CASSSingleObjectApi

All URIs are relative to *https://insertCassUrl/api/data*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_competency**](CASSSingleObjectApi.md#get_competency) | **GET** /insertCassSchemaUrl.0.3.Competency/{competencyId} | Obtains Competencty info.
[**get_framework**](CASSSingleObjectApi.md#get_framework) | **GET** /insertCassSchemaUrl.0.3.Framework/{frameworkId} | Obtains Framework info.
[**get_relation**](CASSSingleObjectApi.md#get_relation) | **GET** /insertCassSchemaUrl.0.3.Relation/{relationId} | Obtains Relation info.


# **get_competency**
> Competency get_competency(competency_id)

Obtains Competencty info.

Obtains the information of the corresponding Competency.

### Example
```python
from __future__ import print_function
import time
import cass_client
from cass_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cass_client.CASSSingleObjectApi()
competency_id = 'competency_id_example' # str | The ID of the requested Competency.

try:
    # Obtains Competencty info.
    api_response = api_instance.get_competency(competency_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CASSSingleObjectApi->get_competency: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **competency_id** | **str**| The ID of the requested Competency. | 

### Return type

[**Competency**](Competency.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_framework**
> Framework get_framework(framework_id)

Obtains Framework info.

Obtains the information of the corresponding Framework.

### Example
```python
from __future__ import print_function
import time
import cass_client
from cass_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cass_client.CASSSingleObjectApi()
framework_id = 'framework_id_example' # str | The ID of the requested Framework.

try:
    # Obtains Framework info.
    api_response = api_instance.get_framework(framework_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CASSSingleObjectApi->get_framework: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **framework_id** | **str**| The ID of the requested Framework. | 

### Return type

[**Framework**](Framework.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_relation**
> Relation get_relation(relation_id)

Obtains Relation info.

Obtains the information of the corresponding Relation.

### Example
```python
from __future__ import print_function
import time
import cass_client
from cass_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = cass_client.CASSSingleObjectApi()
relation_id = 'relation_id_example' # str | The ID of the requested Relation.

try:
    # Obtains Relation info.
    api_response = api_instance.get_relation(relation_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CASSSingleObjectApi->get_relation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **relation_id** | **str**| The ID of the requested Relation. | 

### Return type

[**Relation**](Relation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/ld+json
 - **Accept**: application/ld+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

