# coding: utf-8

"""
    Recommender API

    This is the API definition for the Recommender service.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import recommenderclient
from recommenderclient.api.upcoming_api import UpcomingApi  # noqa: E501
from recommenderclient.rest import ApiException


class TestUpcomingApi(unittest.TestCase):
    """UpcomingApi unit test stubs"""

    def setUp(self):
        self.api = recommenderclient.api.upcoming_api.UpcomingApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_upcoming_get(self):
        """Test case for upcoming_get

        Get upcoming activities  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()