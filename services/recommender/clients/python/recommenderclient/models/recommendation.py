# coding: utf-8

"""
    Recommender API

    This is the API definition for the Recommender service.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from recommenderclient.models.recommendation_row import RecommendationRow  # noqa: F401,E501
from recommenderclient.models.recommended_activity import RecommendedActivity  # noqa: F401,E501


class Recommendation(object):
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
        'type': 'str',
        'timestamp': 'datetime',
        'learner': 'str',
        'assignment': 'RecommendedActivity',
        'recommendations': 'list[RecommendationRow]'
    }

    attribute_map = {
        'type': '_type',
        'timestamp': 'timestamp',
        'learner': 'learner',
        'assignment': 'assignment',
        'recommendations': 'recommendations'
    }

    def __init__(self, type=None, timestamp=None, learner=None, assignment=None, recommendations=None):  # noqa: E501
        """Recommendation - a model defined in Swagger"""  # noqa: E501

        self._type = None
        self._timestamp = None
        self._learner = None
        self._assignment = None
        self._recommendations = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if timestamp is not None:
            self.timestamp = timestamp
        if learner is not None:
            self.learner = learner
        if assignment is not None:
            self.assignment = assignment
        if recommendations is not None:
            self.recommendations = recommendations

    @property
    def type(self):
        """Gets the type of this Recommendation.  # noqa: E501


        :return: The type of this Recommendation.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Recommendation.


        :param type: The type of this Recommendation.  # noqa: E501
        :type: str
        """
        allowed_values = ["Recommendation"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def timestamp(self):
        """Gets the timestamp of this Recommendation.  # noqa: E501

        ISO8601 formatted timestamp  # noqa: E501

        :return: The timestamp of this Recommendation.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this Recommendation.

        ISO8601 formatted timestamp  # noqa: E501

        :param timestamp: The timestamp of this Recommendation.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def learner(self):
        """Gets the learner of this Recommendation.  # noqa: E501

        ID of the learner requesting the recommendation  # noqa: E501

        :return: The learner of this Recommendation.  # noqa: E501
        :rtype: str
        """
        return self._learner

    @learner.setter
    def learner(self, learner):
        """Sets the learner of this Recommendation.

        ID of the learner requesting the recommendation  # noqa: E501

        :param learner: The learner of this Recommendation.  # noqa: E501
        :type: str
        """

        self._learner = learner

    @property
    def assignment(self):
        """Gets the assignment of this Recommendation.  # noqa: E501


        :return: The assignment of this Recommendation.  # noqa: E501
        :rtype: RecommendedActivity
        """
        return self._assignment

    @assignment.setter
    def assignment(self, assignment):
        """Sets the assignment of this Recommendation.


        :param assignment: The assignment of this Recommendation.  # noqa: E501
        :type: RecommendedActivity
        """

        self._assignment = assignment

    @property
    def recommendations(self):
        """Gets the recommendations of this Recommendation.  # noqa: E501

        Array of RecommendationRow objects. Null if assignment is not null.  # noqa: E501

        :return: The recommendations of this Recommendation.  # noqa: E501
        :rtype: list[RecommendationRow]
        """
        return self._recommendations

    @recommendations.setter
    def recommendations(self, recommendations):
        """Sets the recommendations of this Recommendation.

        Array of RecommendationRow objects. Null if assignment is not null.  # noqa: E501

        :param recommendations: The recommendations of this Recommendation.  # noqa: E501
        :type: list[RecommendationRow]
        """

        self._recommendations = recommendations

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
        if not isinstance(other, Recommendation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other