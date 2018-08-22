# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.learner_tokens import LearnerTokens  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTokensController(BaseTestCase):
    """TokensController integration test stubs"""

    def test_delete_learner_tokens(self):
        """Test case for delete_learner_tokens

        Deletes a learner's tokens
        """
        response = self.client.open(
            '/rui-support/tokens/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_learner_tokens(self):
        """Test case for get_learner_tokens

        Obtains the tokens and activity unlock threshold for a learner
        """
        response = self.client.open(
            '/rui-support/tokens/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_learner_tokens(self):
        """Test case for post_learner_tokens

        Adds a new learner to the database with no tokens
        """
        learnerTokensObj = LearnerTokens()
        response = self.client.open(
            '/rui-support/tokens',
            method='POST',
            data=json.dumps(learnerTokensObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_learner_tokens(self):
        """Test case for update_learner_tokens

        Updates a learner's tokens or activity unlock threshold
        """
        learnerTokensObj = LearnerTokens()
        response = self.client.open(
            '/rui-support/tokens/{keycloakId}'.format(keycloakId='keycloakId_example'),
            method='PATCH',
            data=json.dumps(learnerTokensObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
