# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from activity_index_server.models.error import Error  # noqa: E501
from activity_index_server.models.learning_activity import LearningActivity  # noqa: E501
from activity_index_server.test import BaseTestCase


class TestSingleActivityController(BaseTestCase):
    """SingleActivityController integration test stubs"""

    def test_delete_activity(self):
        """Test case for delete_activity

        Deletes a LearningActivity object
        """
        response = self.client.open(
            '/activity-index/activities/{activityId}'.format(activityId='activityId_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_activity(self):
        """Test case for get_activity

        Obtains LearningActivity info
        """
        response = self.client.open(
            '/activity-index/activities/{activityId}'.format(activityId='activityId_example'),
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_activity(self):
        """Test case for post_activity

        Creates a LearningActivity.
        """
        activityObj = LearningActivity()
        response = self.client.open(
            '/activity-index/activities',
            method='POST',
            data=json.dumps(activityObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_activity(self):
        """Test case for update_activity

        Updates LearningActivity info
        """
        activityObj = None
        response = self.client.open(
            '/activity-index/activities/{activityId}'.format(activityId='activityId_example'),
            method='PATCH',
            data=json.dumps(activityObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
