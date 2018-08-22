# coding: utf-8

"""
    Recommender UI Support Service API

    This API is used to interact with the data stored in the Recommender UI Support Service database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PageState(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'learner_keycloak_id': 'str',
        'learner_username': 'str',
        'page_number': 'int'
    }

    attribute_map = {
        'learner_keycloak_id': 'learnerKeycloakId',
        'learner_username': 'learnerUsername',
        'page_number': 'pageNumber'
    }

    def __init__(self, learner_keycloak_id=None, learner_username=None, page_number=None):  # noqa: E501
        """PageState - a model defined in Swagger"""  # noqa: E501

        self._learner_keycloak_id = None
        self._learner_username = None
        self._page_number = None
        self.discriminator = None

        self.learner_keycloak_id = learner_keycloak_id
        if learner_username is not None:
            self.learner_username = learner_username
        self.page_number = page_number

    @property
    def learner_keycloak_id(self):
        """Gets the learner_keycloak_id of this PageState.  # noqa: E501

        The keycloak GUID for the learner (the subject field of the OAUTH object)  # noqa: E501

        :return: The learner_keycloak_id of this PageState.  # noqa: E501
        :rtype: str
        """
        return self._learner_keycloak_id

    @learner_keycloak_id.setter
    def learner_keycloak_id(self, learner_keycloak_id):
        """Sets the learner_keycloak_id of this PageState.

        The keycloak GUID for the learner (the subject field of the OAUTH object)  # noqa: E501

        :param learner_keycloak_id: The learner_keycloak_id of this PageState.  # noqa: E501
        :type: str
        """
        if learner_keycloak_id is None:
            raise ValueError("Invalid value for `learner_keycloak_id`, must not be `None`")  # noqa: E501

        self._learner_keycloak_id = learner_keycloak_id

    @property
    def learner_username(self):
        """Gets the learner_username of this PageState.  # noqa: E501

        The learner's login name  # noqa: E501

        :return: The learner_username of this PageState.  # noqa: E501
        :rtype: str
        """
        return self._learner_username

    @learner_username.setter
    def learner_username(self, learner_username):
        """Sets the learner_username of this PageState.

        The learner's login name  # noqa: E501

        :param learner_username: The learner_username of this PageState.  # noqa: E501
        :type: str
        """

        self._learner_username = learner_username

    @property
    def page_number(self):
        """Gets the page_number of this PageState.  # noqa: E501

        Page number in the UI  # noqa: E501

        :return: The page_number of this PageState.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this PageState.

        Page number in the UI  # noqa: E501

        :param page_number: The page_number of this PageState.  # noqa: E501
        :type: int
        """
        if page_number is None:
            raise ValueError("Invalid value for `page_number`, must not be `None`")  # noqa: E501

        self._page_number = page_number

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PageState):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
