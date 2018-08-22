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


class MasteryProbability(object):
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
        'probability': 'float',
        'timestamp': 'datetime',
        'source': 'str'
    }

    attribute_map = {
        'context': '@context',
        'type': '@type',
        'competency_id': 'competencyId',
        'probability': 'probability',
        'timestamp': 'timestamp',
        'source': 'source'
    }

    def __init__(self, context=None, type=None, competency_id=None, probability=None, timestamp=None, source=None):  # noqa: E501
        """MasteryProbability - a model defined in Swagger"""  # noqa: E501

        self._context = None
        self._type = None
        self._competency_id = None
        self._probability = None
        self._timestamp = None
        self._source = None
        self.discriminator = None

        self.context = context
        self.type = type
        self.competency_id = competency_id
        self.probability = probability
        self.timestamp = timestamp
        self.source = source

    @property
    def context(self):
        """Gets the context of this MasteryProbability.  # noqa: E501

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :return: The context of this MasteryProbability.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this MasteryProbability.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :param context: The context of this MasteryProbability.  # noqa: E501
        :type: str
        """
        if context is None:
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def type(self):
        """Gets the type of this MasteryProbability.  # noqa: E501

        The value of this field will always be \"MasteryProbability\".  # noqa: E501

        :return: The type of this MasteryProbability.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this MasteryProbability.

        The value of this field will always be \"MasteryProbability\".  # noqa: E501

        :param type: The type of this MasteryProbability.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def competency_id(self):
        """Gets the competency_id of this MasteryProbability.  # noqa: E501

        TODO  # noqa: E501

        :return: The competency_id of this MasteryProbability.  # noqa: E501
        :rtype: str
        """
        return self._competency_id

    @competency_id.setter
    def competency_id(self, competency_id):
        """Sets the competency_id of this MasteryProbability.

        TODO  # noqa: E501

        :param competency_id: The competency_id of this MasteryProbability.  # noqa: E501
        :type: str
        """
        if competency_id is None:
            raise ValueError("Invalid value for `competency_id`, must not be `None`")  # noqa: E501

        self._competency_id = competency_id

    @property
    def probability(self):
        """Gets the probability of this MasteryProbability.  # noqa: E501

        TODO  # noqa: E501

        :return: The probability of this MasteryProbability.  # noqa: E501
        :rtype: float
        """
        return self._probability

    @probability.setter
    def probability(self, probability):
        """Sets the probability of this MasteryProbability.

        TODO  # noqa: E501

        :param probability: The probability of this MasteryProbability.  # noqa: E501
        :type: float
        """
        if probability is None:
            raise ValueError("Invalid value for `probability`, must not be `None`")  # noqa: E501

        self._probability = probability

    @property
    def timestamp(self):
        """Gets the timestamp of this MasteryProbability.  # noqa: E501

        TODO  # noqa: E501

        :return: The timestamp of this MasteryProbability.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this MasteryProbability.

        TODO  # noqa: E501

        :param timestamp: The timestamp of this MasteryProbability.  # noqa: E501
        :type: datetime
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def source(self):
        """Gets the source of this MasteryProbability.  # noqa: E501

        Source of the probability estimate.  # noqa: E501

        :return: The source of this MasteryProbability.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this MasteryProbability.

        Source of the probability estimate.  # noqa: E501

        :param source: The source of this MasteryProbability.  # noqa: E501
        :type: str
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source

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
        if not isinstance(other, MasteryProbability):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other