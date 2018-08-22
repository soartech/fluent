# coding: utf-8

"""
    CASS API

    This API is used to interact with the data stored in the CASS database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import cass_client
from cass_client.api.cass_single_object_api import CASSSingleObjectApi  # noqa: E501
from cass_client.rest import ApiException


class TestCASSSingleObjectApi(unittest.TestCase):
    """CASSSingleObjectApi unit test stubs"""

    def setUp(self):
        self.api = cass_client.api.cass_single_object_api.CASSSingleObjectApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_competency(self):
        """Test case for get_competency

        Obtains Competencty info.  # noqa: E501
        """
        pass

    def test_get_framework(self):
        """Test case for get_framework

        Obtains Framework info.  # noqa: E501
        """
        pass

    def test_get_relation(self):
        """Test case for get_relation

        Obtains Relation info.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()