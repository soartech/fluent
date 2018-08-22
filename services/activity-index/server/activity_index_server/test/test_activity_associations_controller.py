# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from activity_index_server.models.error import Error  # noqa: E501
from activity_index_server.test import BaseTestCase


class TestActivityAssociationsController(BaseTestCase):
    """ActivityAssociationsController integration test stubs"""

    def test_get_activity_associations(self):
        """Test case for get_activity_associations

        Obtains mapping of TLOs/ELOs to activities
        """
        response = self.client.open(
            '/activity-index/activity-associations',
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
