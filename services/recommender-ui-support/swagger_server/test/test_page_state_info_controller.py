# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.page_state import PageState  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPageStateInfoController(BaseTestCase):
    """PageStateInfoController integration test stubs"""

    def test_delete_page_state(self):
        """Test case for delete_page_state

        Deletes the page state for a user session
        """
        response = self.client.open(
            '/rui_support/page-state/{tempIdentifier}'.format(tempIdentifier='tempIdentifier_example'),
            method='DELETE',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_page_state(self):
        """Test case for get_page_state

        Obtains the page state for a user session
        """
        response = self.client.open(
            '/rui_support/page-state/{tempIdentifier}'.format(tempIdentifier='tempIdentifier_example'),
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_page_state(self):
        """Test case for post_page_state

        Stores the page state for a new user session
        """
        pageStateObj = PageState()
        response = self.client.open(
            '/rui_support/page-state',
            method='POST',
            data=json.dumps(pageStateObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_page_state(self):
        """Test case for update_page_state

        Updates the page state for a user session
        """
        pageStateObj = PageState()
        response = self.client.open(
            '/rui_support/page-state/{tempIdentifier}'.format(tempIdentifier='tempIdentifier_example'),
            method='PATCH',
            data=json.dumps(pageStateObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
