# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from learner_inferences_server.models.error import Error  # noqa: E501
from learner_inferences_server.models.learner import Learner  # noqa: E501
from learner_inferences_server.test import BaseTestCase


class TestMultipleLearnersController(BaseTestCase):
    """MultipleLearnersController integration test stubs"""

    def test_get_learners(self):
        """Test case for get_learners

        Obtains a collection of Learner objects from Learner Profile.
        """
        query_string = [('limit', 56),
                        ('offset', 56)]
        response = self.client.open(
            '/learner-inferences/learners',
            method='GET',
            content_type='application/ld+json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
