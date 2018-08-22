# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.learner_goals import LearnerGoals  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLearnerGoalsController(BaseTestCase):
    """LearnerGoalsController integration test stubs"""

    def test_update_goals(self):
        """Test case for update_goals

        Updates the goals for a learner
        """
        learnerGoalsObj = LearnerGoals()
        response = self.client.open(
            '/rui-support/learner-goals/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='PATCH',
            data=json.dumps(learnerGoalsObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
