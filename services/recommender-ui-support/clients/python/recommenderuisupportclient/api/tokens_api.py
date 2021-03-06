# coding: utf-8

"""
    Recommender UI Support Service API

    This API is used to interact with the data stored in the Recommender UI Support Service database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from recommenderuisupportclient.api_client import ApiClient


class TokensApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_learner_tokens(self, keycloak_id, **kwargs):  # noqa: E501
        """Deletes a learner&#39;s tokens  # noqa: E501

        Removes the learner from the database  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.delete_learner_tokens(keycloak_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.delete_learner_tokens_with_http_info(keycloak_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_learner_tokens_with_http_info(keycloak_id, **kwargs)  # noqa: E501
            return data

    def delete_learner_tokens_with_http_info(self, keycloak_id, **kwargs):  # noqa: E501
        """Deletes a learner&#39;s tokens  # noqa: E501

        Removes the learner from the database  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.delete_learner_tokens_with_http_info(keycloak_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['keycloak_id']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_learner_tokens" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'keycloak_id' is set
        if ('keycloak_id' not in params or
                params['keycloak_id'] is None):
            raise ValueError("Missing the required parameter `keycloak_id` when calling `delete_learner_tokens`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'keycloak_id' in params:
            path_params['keycloakId'] = params['keycloak_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/ld+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/ld+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tokens/{keycloakId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_learner_tokens(self, keycloak_id, **kwargs):  # noqa: E501
        """Obtains the tokens for a learner  # noqa: E501

        Returns the set of tokens the learner has earned so far  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_learner_tokens(keycloak_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose tokens will be returned (required)
        :return: LearnerTokens
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_learner_tokens_with_http_info(keycloak_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_learner_tokens_with_http_info(keycloak_id, **kwargs)  # noqa: E501
            return data

    def get_learner_tokens_with_http_info(self, keycloak_id, **kwargs):  # noqa: E501
        """Obtains the tokens for a learner  # noqa: E501

        Returns the set of tokens the learner has earned so far  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_learner_tokens_with_http_info(keycloak_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose tokens will be returned (required)
        :return: LearnerTokens
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['keycloak_id']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_learner_tokens" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'keycloak_id' is set
        if ('keycloak_id' not in params or
                params['keycloak_id'] is None):
            raise ValueError("Missing the required parameter `keycloak_id` when calling `get_learner_tokens`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'keycloak_id' in params:
            path_params['keycloakId'] = params['keycloak_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/ld+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/ld+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tokens/{keycloakId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LearnerTokens',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_learner_tokens(self, learner_tokens_obj, **kwargs):  # noqa: E501
        """Adds a new learner to the database with no tokens  # noqa: E501

        Adds a new learner to the database with an empty set of tokens  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.post_learner_tokens(learner_tokens_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param LearnerTokens learner_tokens_obj: LearnerTokens object to add (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.post_learner_tokens_with_http_info(learner_tokens_obj, **kwargs)  # noqa: E501
        else:
            (data) = self.post_learner_tokens_with_http_info(learner_tokens_obj, **kwargs)  # noqa: E501
            return data

    def post_learner_tokens_with_http_info(self, learner_tokens_obj, **kwargs):  # noqa: E501
        """Adds a new learner to the database with no tokens  # noqa: E501

        Adds a new learner to the database with an empty set of tokens  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.post_learner_tokens_with_http_info(learner_tokens_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param LearnerTokens learner_tokens_obj: LearnerTokens object to add (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['learner_tokens_obj']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_learner_tokens" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'learner_tokens_obj' is set
        if ('learner_tokens_obj' not in params or
                params['learner_tokens_obj'] is None):
            raise ValueError("Missing the required parameter `learner_tokens_obj` when calling `post_learner_tokens`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'learner_tokens_obj' in params:
            body_params = params['learner_tokens_obj']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/ld+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/ld+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tokens', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_learner_tokens(self, keycloak_id, learner_tokens_obj, **kwargs):  # noqa: E501
        """Updates a learner&#39;s tokens  # noqa: E501

        Adds some tokens to the learner's current set of tokens  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.update_learner_tokens(keycloak_id, learner_tokens_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose tokens will be updated (required)
        :param LearnerTokens learner_tokens_obj: LearnerTokens object to update (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.update_learner_tokens_with_http_info(keycloak_id, learner_tokens_obj, **kwargs)  # noqa: E501
        else:
            (data) = self.update_learner_tokens_with_http_info(keycloak_id, learner_tokens_obj, **kwargs)  # noqa: E501
            return data

    def update_learner_tokens_with_http_info(self, keycloak_id, learner_tokens_obj, **kwargs):  # noqa: E501
        """Updates a learner&#39;s tokens  # noqa: E501

        Adds some tokens to the learner's current set of tokens  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.update_learner_tokens_with_http_info(keycloak_id, learner_tokens_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose tokens will be updated (required)
        :param LearnerTokens learner_tokens_obj: LearnerTokens object to update (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['keycloak_id', 'learner_tokens_obj']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_learner_tokens" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'keycloak_id' is set
        if ('keycloak_id' not in params or
                params['keycloak_id'] is None):
            raise ValueError("Missing the required parameter `keycloak_id` when calling `update_learner_tokens`")  # noqa: E501
        # verify the required parameter 'learner_tokens_obj' is set
        if ('learner_tokens_obj' not in params or
                params['learner_tokens_obj'] is None):
            raise ValueError("Missing the required parameter `learner_tokens_obj` when calling `update_learner_tokens`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'keycloak_id' in params:
            path_params['keycloakId'] = params['keycloak_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'learner_tokens_obj' in params:
            body_params = params['learner_tokens_obj']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/ld+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/ld+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/tokens/{keycloakId}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
