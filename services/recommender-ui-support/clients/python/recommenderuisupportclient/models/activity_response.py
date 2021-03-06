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


class ActivityResponse(object):
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
        'timestamp': 'datetime',
        'popularity_rating': 'int',
        'emotion_rating': 'str'
    }

    attribute_map = {
        'learner_keycloak_id': 'learnerKeycloakId',
        'timestamp': 'timestamp',
        'popularity_rating': 'popularityRating',
        'emotion_rating': 'emotionRating'
    }

    def __init__(self, learner_keycloak_id=None, timestamp=None, popularity_rating=None, emotion_rating=None):  # noqa: E501
        """ActivityResponse - a model defined in Swagger"""  # noqa: E501

        self._learner_keycloak_id = None
        self._timestamp = None
        self._popularity_rating = None
        self._emotion_rating = None
        self.discriminator = None

        self.learner_keycloak_id = learner_keycloak_id
        self.timestamp = timestamp
        self.popularity_rating = popularity_rating
        self.emotion_rating = emotion_rating

    @property
    def learner_keycloak_id(self):
        """Gets the learner_keycloak_id of this ActivityResponse.  # noqa: E501

        The keycloak GUID for the learner (the subject field of the OAUTH object)  # noqa: E501

        :return: The learner_keycloak_id of this ActivityResponse.  # noqa: E501
        :rtype: str
        """
        return self._learner_keycloak_id

    @learner_keycloak_id.setter
    def learner_keycloak_id(self, learner_keycloak_id):
        """Sets the learner_keycloak_id of this ActivityResponse.

        The keycloak GUID for the learner (the subject field of the OAUTH object)  # noqa: E501

        :param learner_keycloak_id: The learner_keycloak_id of this ActivityResponse.  # noqa: E501
        :type: str
        """
        if learner_keycloak_id is None:
            raise ValueError("Invalid value for `learner_keycloak_id`, must not be `None`")  # noqa: E501

        self._learner_keycloak_id = learner_keycloak_id

    @property
    def timestamp(self):
        """Gets the timestamp of this ActivityResponse.  # noqa: E501

        The date and time this response was recorded  # noqa: E501

        :return: The timestamp of this ActivityResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this ActivityResponse.

        The date and time this response was recorded  # noqa: E501

        :param timestamp: The timestamp of this ActivityResponse.  # noqa: E501
        :type: datetime
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def popularity_rating(self):
        """Gets the popularity_rating of this ActivityResponse.  # noqa: E501

        Personal rating for the activity on a scale from 1 to 5  # noqa: E501

        :return: The popularity_rating of this ActivityResponse.  # noqa: E501
        :rtype: int
        """
        return self._popularity_rating

    @popularity_rating.setter
    def popularity_rating(self, popularity_rating):
        """Sets the popularity_rating of this ActivityResponse.

        Personal rating for the activity on a scale from 1 to 5  # noqa: E501

        :param popularity_rating: The popularity_rating of this ActivityResponse.  # noqa: E501
        :type: int
        """
        if popularity_rating is None:
            raise ValueError("Invalid value for `popularity_rating`, must not be `None`")  # noqa: E501

        self._popularity_rating = popularity_rating

    @property
    def emotion_rating(self):
        """Gets the emotion_rating of this ActivityResponse.  # noqa: E501

        Was the activity boring, confusing, frustrating, pleasant, epic, or neutral?  # noqa: E501

        :return: The emotion_rating of this ActivityResponse.  # noqa: E501
        :rtype: str
        """
        return self._emotion_rating

    @emotion_rating.setter
    def emotion_rating(self, emotion_rating):
        """Sets the emotion_rating of this ActivityResponse.

        Was the activity boring, confusing, frustrating, pleasant, epic, or neutral?  # noqa: E501

        :param emotion_rating: The emotion_rating of this ActivityResponse.  # noqa: E501
        :type: str
        """
        if emotion_rating is None:
            raise ValueError("Invalid value for `emotion_rating`, must not be `None`")  # noqa: E501

        self._emotion_rating = emotion_rating

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
        if not isinstance(other, ActivityResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
