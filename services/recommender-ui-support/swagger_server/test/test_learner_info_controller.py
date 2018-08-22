# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.learner_preferences import LearnerPreferences  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLearnerInfoController(BaseTestCase):
    """LearnerInfoController integration test stubs"""

    def test_delete_learner_preferences(self):
        """Test case for delete_learner_preferences

        Deletes a learner's preferences
        """
        response = self.client.open(
            '/rui_support/learner-preferences/{learnerId}'.format(learnerId='learnerId_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_learner_preference(self):
        """Test case for post_learner_preference

        Stores a learner's preferences
        """
        learnerPreferenceObj = LearnerPreferences()
        response = self.client.open(
            '/rui_support/learner-preferences',
            method='POST',
            data=json.dumps(learnerPreferenceObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_learner_preferences(self):
        """Test case for update_learner_preferences

        Updates a learner's preferences
        """
        learnerPreferenceObj = LearnerPreferences()
        response = self.client.open(
            '/rui_support/learner-preferences/{learnerId}'.format(learnerId='learnerId_example'),
            method='PATCH',
            data=json.dumps(learnerPreferenceObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
