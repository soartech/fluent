# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.ao_image import AoImage  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAOImageController(BaseTestCase):
    """AOImageController integration test stubs"""

    def test_get_ao_image(self):
        """Test case for get_ao_image

        Obtains the AO Image
        """
        response = self.client.open(
            '/rui-support/ao-image',
            method='GET',
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_ao_image(self):
        """Test case for post_ao_image

        Stores the AO Image
        """
        aoImageObj = AoImage()
        response = self.client.open(
            '/rui-support/ao-image',
            method='POST',
            data=json.dumps(aoImageObj),
            content_type='application/ld+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
