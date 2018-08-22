# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.learner_preferences import LearnerPreferences  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLearnerPreferencesController(BaseTestCase):
    """LearnerPreferencesController integration test stubs"""

    def test_delete_learner_preferences(self):
        """Test case for delete_learner_preferences

        Deletes a learner's preferences
        """
        response = self.client.open(
            '/rui-support/learner-preferences/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_learner_preferences(self):
        """Test case for post_learner_preferences

        Stores a learner's preferences
        """
        learnerPreferencesObj = LearnerPreferences()
        response = self.client.open(
            '/rui-support/learner-preferences/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='POST',
            data=json.dumps(learnerPreferencesObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_learner_preferences(self):
        """Test case for update_learner_preferences

        Updates a learner's preferences
        """
        learnerPreferencesObj = LearnerPreferences()
        response = self.client.open(
            '/rui-support/learner-preferences/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='PATCH',
            data=json.dumps(learnerPreferencesObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
