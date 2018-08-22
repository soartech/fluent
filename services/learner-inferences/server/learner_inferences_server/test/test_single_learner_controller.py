# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from learner_inferences_server.models.error import Error  # noqa: E501
from learner_inferences_server.models.learner import Learner  # noqa: E501
from learner_inferences_server.test import BaseTestCase


class TestSingleLearnerController(BaseTestCase):
    """SingleLearnerController integration test stubs"""

    def test_delete_learner(self):
        """Test case for delete_learner

        Deletes a Learner object.
        """
        response = self.client.open(
            '/learner-inferences/learners/{learnerId}'.format(learnerId='learnerId_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_learner(self):
        """Test case for get_learner

        Obtains Learner info.
        """
        response = self.client.open(
            '/learner-inferences/learners/{learnerId}'.format(learnerId='learnerId_example'),
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_learner(self):
        """Test case for post_learner

        Creates one Learner in Learner Profile.
        """
        learnerObj = Learner()
        response = self.client.open(
            '/learner-inferences/learners/{learnerId}',
            method='POST',
            data=json.dumps(learnerObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_learner(self):
        """Test case for update_learner

        Updates Learner info.
        """
        learnerObj = Learner()
        response = self.client.open(
            '/learner-inferences/learners/{learnerId}'.format(learnerId='learnerId_example'),
            method='PATCH',
            data=json.dumps(learnerObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
