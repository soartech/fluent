# coding: utf-8

"""
    Asset API

    This API is used to interact with the data stored in the TLA Activity Index database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import activity_index_client
from activity_index_client.api.single_activity_api import SingleActivityApi  # noqa: E501
from activity_index_client.rest import ApiException


class TestSingleActivityApi(unittest.TestCase):
    """SingleActivityApi unit test stubs"""

    def setUp(self):
        self.api = activity_index_client.api.single_activity_api.SingleActivityApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_activity(self):
        """Test case for delete_activity

        Deletes a LearningActivity object  # noqa: E501
        """
        pass

    def test_get_activity(self):
        """Test case for get_activity

        Obtains LearningActivity info  # noqa: E501
        """
        pass

    def test_post_activity(self):
        """Test case for post_activity

        Creates a LearningActivity.  # noqa: E501
        """
        pass

    def test_update_activity(self):
        """Test case for update_activity

        Updates LearningActivity info  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
