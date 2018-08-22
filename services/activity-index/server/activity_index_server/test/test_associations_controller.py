# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from activity_index_server.models.competency_associations import CompetencyAssociations  # noqa: E501
from activity_index_server.models.error import Error  # noqa: E501
from activity_index_server.models.token_associations import TokenAssociations  # noqa: E501
from activity_index_server.test import BaseTestCase


class TestAssociationsController(BaseTestCase):
    """AssociationsController integration test stubs"""

    def test_generate_associations(self):
        """Test case for generate_associations

        Generates mapping from TLOs/ELOs to activities and token types to activities
        """
        response = self.client.open(
            '/activity-index/associations',
            method='POST',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_competency_associations(self):
        """Test case for get_competency_associations

        Obtains mapping of TLOs/ELOs to activities
        """
        response = self.client.open(
            '/activity-index/competency-associations',
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_token_associations(self):
        """Test case for get_token_associations

        Obtains mapping of token types to activities
        """
        response = self.client.open(
            '/activity-index/token-associations',
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
