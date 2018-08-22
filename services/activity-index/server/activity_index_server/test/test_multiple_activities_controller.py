# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from activity_index_server.models.error import Error  # noqa: E501
from activity_index_server.models.learning_activity import LearningActivity  # noqa: E501
from activity_index_server.test import BaseTestCase


class TestMultipleActivitiesController(BaseTestCase):
    """MultipleActivitiesController integration test stubs"""

    def test_get_activities(self):
        """Test case for get_activities

        Obtains multiple LearningActivity objects
        """
        query_string = [('limit', 56),
                        ('offset', 56)]
        response = self.client.open(
            '/activity-index/activities',
            method='GET',
            content_type='application/ld+json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
