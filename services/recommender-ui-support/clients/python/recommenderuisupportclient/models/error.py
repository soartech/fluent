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


class Error(object):
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
        'error_message': 'str',
        'error_code': 'str',
        'error_link': 'str',
        'user_message': 'str'
    }

    attribute_map = {
        'error_message': 'errorMessage',
        'error_code': 'errorCode',
        'error_link': 'errorLink',
        'user_message': 'userMessage'
    }

    def __init__(self, error_message=None, error_code=None, error_link=None, user_message=None):  # noqa: E501
        """Error - a model defined in Swagger"""  # noqa: E501

        self._error_message = None
        self._error_code = None
        self._error_link = None
        self._user_message = None
        self.discriminator = None

        self.error_message = error_message
        if error_code is not None:
            self.error_code = error_code
        if error_link is not None:
            self.error_link = error_link
        if user_message is not None:
            self.user_message = user_message

    @property
    def error_message(self):
        """Gets the error_message of this Error.  # noqa: E501


        :return: The error_message of this Error.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this Error.


        :param error_message: The error_message of this Error.  # noqa: E501
        :type: str
        """
        if error_message is None:
            raise ValueError("Invalid value for `error_message`, must not be `None`")  # noqa: E501

        self._error_message = error_message

    @property
    def error_code(self):
        """Gets the error_code of this Error.  # noqa: E501


        :return: The error_code of this Error.  # noqa: E501
        :rtype: str
        """
        return self._error_code

    @error_code.setter
    def error_code(self, error_code):
        """Sets the error_code of this Error.


        :param error_code: The error_code of this Error.  # noqa: E501
        :type: str
        """

        self._error_code = error_code

    @property
    def error_link(self):
        """Gets the error_link of this Error.  # noqa: E501


        :return: The error_link of this Error.  # noqa: E501
        :rtype: str
        """
        return self._error_link

    @error_link.setter
    def error_link(self, error_link):
        """Sets the error_link of this Error.


        :param error_link: The error_link of this Error.  # noqa: E501
        :type: str
        """

        self._error_link = error_link

    @property
    def user_message(self):
        """Gets the user_message of this Error.  # noqa: E501


        :return: The user_message of this Error.  # noqa: E501
        :rtype: str
        """
        return self._user_message

    @user_message.setter
    def user_message(self, user_message):
        """Sets the user_message of this Error.


        :param user_message: The user_message of this Error.  # noqa: E501
        :type: str
        """

        self._user_message = user_message

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
        if not isinstance(other, Error):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
