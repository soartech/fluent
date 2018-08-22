# coding: utf-8

"""
    Recommender API

    This is the API definition for the Recommender service.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from recommenderclient.api_client import ApiClient


class UpcomingApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def upcoming_get(self, learner_id, **kwargs):  # noqa: E501
        """Get upcoming activities  # noqa: E501

        Returns an overview of what the learner will be working on (and reflected in upcoming recommendations). It should include current ELO in the sequence that the learner has not yet mastered that they will continue learning. It will also include any ELOs that the learner has forgotten that will be reviewed.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.upcoming_get(learner_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str learner_id: Id of the learner to get a recommendation for (required)
        :return: Recommendation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.upcoming_get_with_http_info(learner_id, **kwargs)  # noqa: E501
        else:
            (data) = self.upcoming_get_with_http_info(learner_id, **kwargs)  # noqa: E501
            return data

    def upcoming_get_with_http_info(self, learner_id, **kwargs):  # noqa: E501
        """Get upcoming activities  # noqa: E501

        Returns an overview of what the learner will be working on (and reflected in upcoming recommendations). It should include current ELO in the sequence that the learner has not yet mastered that they will continue learning. It will also include any ELOs that the learner has forgotten that will be reviewed.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.upcoming_get_with_http_info(learner_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str learner_id: Id of the learner to get a recommendation for (required)
        :return: Recommendation
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['learner_id']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upcoming_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'learner_id' is set
        if ('learner_id' not in params or
                params['learner_id'] is None):
            raise ValueError("Missing the required parameter `learner_id` when calling `upcoming_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'learner_id' in params:
            query_params.append(('learnerId', params['learner_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/upcoming', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Recommendation',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
