# coding: utf-8

"""
    Recommender UI Support Service API

    This API is used to interact with the data stored in the Recommnder UI Support Service database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from recommenderuisupportclient.api_client import ApiClient


class LearnerPreferencesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_learner_preferences(self, keycloak_id, **kwargs):  # noqa: E501
        """Deletes a learner&#39;s preferences  # noqa: E501

        Removes the learner from the database  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.delete_learner_preferences(keycloak_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.delete_learner_preferences_with_http_info(keycloak_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_learner_preferences_with_http_info(keycloak_id, **kwargs)  # noqa: E501
            return data

    def delete_learner_preferences_with_http_info(self, keycloak_id, **kwargs):  # noqa: E501
        """Deletes a learner&#39;s preferences  # noqa: E501

        Removes the learner from the database  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.delete_learner_preferences_with_http_info(keycloak_id, async=True)
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
                    " to method delete_learner_preferences" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'keycloak_id' is set
        if ('keycloak_id' not in params or
                params['keycloak_id'] is None):
            raise ValueError("Missing the required parameter `keycloak_id` when calling `delete_learner_preferences`")  # noqa: E501

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
            '/learner-preferences/{keycloakId}', 'DELETE',
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

    def post_learner_preferences(self, keycloak_id, learner_preferences_obj, **kwargs):  # noqa: E501
        """Stores a learner&#39;s preferences  # noqa: E501

        Adds a new learner to the database along with their initial preferences  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.post_learner_preferences(keycloak_id, learner_preferences_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose preferences will be added (required)
        :param LearnerPreferences learner_preferences_obj: LearnerPreferences object to add (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.post_learner_preferences_with_http_info(keycloak_id, learner_preferences_obj, **kwargs)  # noqa: E501
        else:
            (data) = self.post_learner_preferences_with_http_info(keycloak_id, learner_preferences_obj, **kwargs)  # noqa: E501
            return data

    def post_learner_preferences_with_http_info(self, keycloak_id, learner_preferences_obj, **kwargs):  # noqa: E501
        """Stores a learner&#39;s preferences  # noqa: E501

        Adds a new learner to the database along with their initial preferences  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.post_learner_preferences_with_http_info(keycloak_id, learner_preferences_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose preferences will be added (required)
        :param LearnerPreferences learner_preferences_obj: LearnerPreferences object to add (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['keycloak_id', 'learner_preferences_obj']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_learner_preferences" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'keycloak_id' is set
        if ('keycloak_id' not in params or
                params['keycloak_id'] is None):
            raise ValueError("Missing the required parameter `keycloak_id` when calling `post_learner_preferences`")  # noqa: E501
        # verify the required parameter 'learner_preferences_obj' is set
        if ('learner_preferences_obj' not in params or
                params['learner_preferences_obj'] is None):
            raise ValueError("Missing the required parameter `learner_preferences_obj` when calling `post_learner_preferences`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'keycloak_id' in params:
            path_params['keycloakId'] = params['keycloak_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'learner_preferences_obj' in params:
            body_params = params['learner_preferences_obj']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/ld+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/ld+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/learner-preferences/{keycloakId}', 'POST',
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

    def update_learner_preferences(self, keycloak_id, learner_preferences_obj, **kwargs):  # noqa: E501
        """Updates a learner&#39;s preferences  # noqa: E501

        Updates the learner's preferences in the database  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.update_learner_preferences(keycloak_id, learner_preferences_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose preferences will be updated (required)
        :param LearnerPreferences learner_preferences_obj: LearnerPreferences object to update (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.update_learner_preferences_with_http_info(keycloak_id, learner_preferences_obj, **kwargs)  # noqa: E501
        else:
            (data) = self.update_learner_preferences_with_http_info(keycloak_id, learner_preferences_obj, **kwargs)  # noqa: E501
            return data

    def update_learner_preferences_with_http_info(self, keycloak_id, learner_preferences_obj, **kwargs):  # noqa: E501
        """Updates a learner&#39;s preferences  # noqa: E501

        Updates the learner's preferences in the database  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.update_learner_preferences_with_http_info(keycloak_id, learner_preferences_obj, async=True)
        >>> result = thread.get()

        :param async bool
        :param str keycloak_id: The ID of the learner whose preferences will be updated (required)
        :param LearnerPreferences learner_preferences_obj: LearnerPreferences object to update (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['keycloak_id', 'learner_preferences_obj']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_learner_preferences" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'keycloak_id' is set
        if ('keycloak_id' not in params or
                params['keycloak_id'] is None):
            raise ValueError("Missing the required parameter `keycloak_id` when calling `update_learner_preferences`")  # noqa: E501
        # verify the required parameter 'learner_preferences_obj' is set
        if ('learner_preferences_obj' not in params or
                params['learner_preferences_obj'] is None):
            raise ValueError("Missing the required parameter `learner_preferences_obj` when calling `update_learner_preferences`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'keycloak_id' in params:
            path_params['keycloakId'] = params['keycloak_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'learner_preferences_obj' in params:
            body_params = params['learner_preferences_obj']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/ld+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/ld+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/learner-preferences/{keycloakId}', 'PATCH',
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
