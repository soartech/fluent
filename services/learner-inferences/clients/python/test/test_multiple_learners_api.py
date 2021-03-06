# coding: utf-8

"""
    Learner API

    This API is used to interact with the data stored in the TLA Learner Profile database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import learner_inferences_client
from learner_inferences_client.api.multiple_learners_api import MultipleLearnersApi  # noqa: E501
from learner_inferences_client.rest import ApiException


class TestMultipleLearnersApi(unittest.TestCase):
    """MultipleLearnersApi unit test stubs"""

    def setUp(self):
        self.api = learner_inferences_client.api.multiple_learners_api.MultipleLearnersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_learners(self):
        """Test case for get_learners

        Obtains a collection of Learner objects from Learner Profile.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
