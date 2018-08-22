# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from recommenderserver.models.recommendation import Recommendation  # noqa: E501
from recommenderserver.test import BaseTestCase


class TestAllController(BaseTestCase):
    """AllController integration test stubs"""

    def test_all_get(self):
        """Test case for all_get

        Get all activities
        """
        query_string = [('learnerId', 'learnerId_example')]
        response = self.client.open(
            '/recommender/all',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
