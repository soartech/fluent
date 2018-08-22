# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.activity_response import ActivityResponse  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestActivityInfoController(BaseTestCase):
    """ActivityInfoController integration test stubs"""

    def test_delete_activity_response(self):
        """Test case for delete_activity_response

        Deletes an activity and all its responses
        """
        response = self.client.open(
            '/rui_support/activity-responses/{activityId}'.format(activityId='activityId_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_activity_response(self):
        """Test case for post_activity_response

        Stores an activity self-report response
        """
        activityResponseObj = ActivityResponse()
        response = self.client.open(
            '/rui_support/activity-responses/{activityId}'.format(activityId='activityId_example'),
            method='POST',
            data=json.dumps(activityResponseObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
