# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from recommenderserver.models.recommendation import Recommendation  # noqa: E501
from recommenderserver.test import BaseTestCase


class TestRecommendationController(BaseTestCase):
    """RecommendationController integration test stubs"""

    def test_recommendation_get(self):
        """Test case for recommendation_get

        Get a new recommendation
        """
        query_string = [('learnerId', 'learnerId_example')]
        response = self.client.open(
            '/recommender/recommendation',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
