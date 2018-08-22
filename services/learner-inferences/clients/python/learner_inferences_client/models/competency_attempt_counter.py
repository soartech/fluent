# coding: utf-8

"""
    Learner API

    This API is used to interact with the data stored in the TLA Learner Profile database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class CompetencyAttemptCounter(object):
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
        'context': 'str',
        'type': 'str',
        'competency_id': 'str',
        'attempts': 'float',
        'last_attempt_date_time': 'datetime'
    }

    attribute_map = {
        'context': '@context',
        'type': '@type',
        'competency_id': 'competencyId',
        'attempts': 'attempts',
        'last_attempt_date_time': 'lastAttemptDateTime'
    }

    def __init__(self, context=None, type=None, competency_id=None, attempts=None, last_attempt_date_time=None):  # noqa: E501
        """CompetencyAttemptCounter - a model defined in Swagger"""  # noqa: E501

        self._context = None
        self._type = None
        self._competency_id = None
        self._attempts = None
        self._last_attempt_date_time = None
        self.discriminator = None

        self.context = context
        self.type = type
        self.competency_id = competency_id
        self.attempts = attempts
        if last_attempt_date_time is not None:
            self.last_attempt_date_time = last_attempt_date_time

    @property
    def context(self):
        """Gets the context of this CompetencyAttemptCounter.  # noqa: E501

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :return: The context of this CompetencyAttemptCounter.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this CompetencyAttemptCounter.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :param context: The context of this CompetencyAttemptCounter.  # noqa: E501
        :type: str
        """
        if context is None:
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def type(self):
        """Gets the type of this CompetencyAttemptCounter.  # noqa: E501

        The value of this field will always be \"CompetencyAttemptCounter\".  # noqa: E501

        :return: The type of this CompetencyAttemptCounter.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CompetencyAttemptCounter.

        The value of this field will always be \"CompetencyAttemptCounter\".  # noqa: E501

        :param type: The type of this CompetencyAttemptCounter.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def competency_id(self):
        """Gets the competency_id of this CompetencyAttemptCounter.  # noqa: E501

        TODO  # noqa: E501

        :return: The competency_id of this CompetencyAttemptCounter.  # noqa: E501
        :rtype: str
        """
        return self._competency_id

    @competency_id.setter
    def competency_id(self, competency_id):
        """Sets the competency_id of this CompetencyAttemptCounter.

        TODO  # noqa: E501

        :param competency_id: The competency_id of this CompetencyAttemptCounter.  # noqa: E501
        :type: str
        """
        if competency_id is None:
            raise ValueError("Invalid value for `competency_id`, must not be `None`")  # noqa: E501

        self._competency_id = competency_id

    @property
    def attempts(self):
        """Gets the attempts of this CompetencyAttemptCounter.  # noqa: E501


        :return: The attempts of this CompetencyAttemptCounter.  # noqa: E501
        :rtype: float
        """
        return self._attempts

    @attempts.setter
    def attempts(self, attempts):
        """Sets the attempts of this CompetencyAttemptCounter.


        :param attempts: The attempts of this CompetencyAttemptCounter.  # noqa: E501
        :type: float
        """
        if attempts is None:
            raise ValueError("Invalid value for `attempts`, must not be `None`")  # noqa: E501

        self._attempts = attempts

    @property
    def last_attempt_date_time(self):
        """Gets the last_attempt_date_time of this CompetencyAttemptCounter.  # noqa: E501

        TODO  # noqa: E501

        :return: The last_attempt_date_time of this CompetencyAttemptCounter.  # noqa: E501
        :rtype: datetime
        """
        return self._last_attempt_date_time

    @last_attempt_date_time.setter
    def last_attempt_date_time(self, last_attempt_date_time):
        """Sets the last_attempt_date_time of this CompetencyAttemptCounter.

        TODO  # noqa: E501

        :param last_attempt_date_time: The last_attempt_date_time of this CompetencyAttemptCounter.  # noqa: E501
        :type: datetime
        """

        self._last_attempt_date_time = last_attempt_date_time

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
        if not isinstance(other, CompetencyAttemptCounter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other