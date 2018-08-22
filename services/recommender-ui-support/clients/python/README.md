# recommenderuisupportclient
This API is used to interact with the data stored in the Recommender UI Support Service database.

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 0.1.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import recommenderuisupportclient 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import recommenderuisupportclient
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

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

## Documentation for API Endpoints

All URIs are relative to *https://fluent.tla/rui-support*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AOImageApi* | [**get_ao_image**](docs/AOImageApi.md#get_ao_image) | **GET** /ao-image | Obtains the AO Image
*AOImageApi* | [**post_ao_image**](docs/AOImageApi.md#post_ao_image) | **POST** /ao-image | Stores the AO Image
*ActivityResponsesApi* | [**delete_activity_response**](docs/ActivityResponsesApi.md#delete_activity_response) | **DELETE** /activity-responses/{activityId} | Deletes an activity and all its responses
*ActivityResponsesApi* | [**post_activity_response**](docs/ActivityResponsesApi.md#post_activity_response) | **POST** /activity-responses | Stores an activity self-report response
*PageStateApi* | [**delete_page_state**](docs/PageStateApi.md#delete_page_state) | **DELETE** /page-state/{keycloakId} | Deletes the page state for a user session
*PageStateApi* | [**get_page_state**](docs/PageStateApi.md#get_page_state) | **GET** /page-state/{keycloakId} | Obtains the page state for a user session
*PageStateApi* | [**post_page_state**](docs/PageStateApi.md#post_page_state) | **POST** /page-state | Stores the page state for a new user session
*PageStateApi* | [**update_page_state**](docs/PageStateApi.md#update_page_state) | **PATCH** /page-state/{keycloakId} | Updates the page state for a user session
*TokensApi* | [**delete_learner_tokens**](docs/TokensApi.md#delete_learner_tokens) | **DELETE** /tokens/{keycloakId} | Deletes a learner&#39;s tokens
*TokensApi* | [**get_learner_tokens**](docs/TokensApi.md#get_learner_tokens) | **GET** /tokens/{keycloakId} | Obtains the tokens for a learner
*TokensApi* | [**post_learner_tokens**](docs/TokensApi.md#post_learner_tokens) | **POST** /tokens | Adds a new learner to the database with no tokens
*TokensApi* | [**update_learner_tokens**](docs/TokensApi.md#update_learner_tokens) | **PATCH** /tokens/{keycloakId} | Updates a learner&#39;s tokens


## Documentation For Models

 - [ActivityResponse](docs/ActivityResponse.md)
 - [ActivityTokens](docs/ActivityTokens.md)
 - [AoImage](docs/AoImage.md)
 - [Error](docs/Error.md)
 - [LearnerTokens](docs/LearnerTokens.md)
 - [PageState](docs/PageState.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author


