# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from learner_inferences_server.models.base_model_ import Model
from learner_inferences_server import util


class ActivityAttemptCounter(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, context: str=None, type: str=None, activity_id: str=None, attempts: float=None, last_attempt_date_time: datetime=None):  # noqa: E501
        """ActivityAttemptCounter - a model defined in Swagger

        :param context: The context of this ActivityAttemptCounter.  # noqa: E501
        :type context: str
        :param type: The type of this ActivityAttemptCounter.  # noqa: E501
        :type type: str
        :param activity_id: The activity_id of this ActivityAttemptCounter.  # noqa: E501
        :type activity_id: str
        :param attempts: The attempts of this ActivityAttemptCounter.  # noqa: E501
        :type attempts: float
        :param last_attempt_date_time: The last_attempt_date_time of this ActivityAttemptCounter.  # noqa: E501
        :type last_attempt_date_time: datetime
        """
        self.swagger_types = {
            'context': str,
            'type': str,
            'activity_id': str,
            'attempts': float,
            'last_attempt_date_time': datetime
        }

        self.attribute_map = {
            'context': '@context',
            'type': '@type',
            'activity_id': 'activityId',
            'attempts': 'attempts',
            'last_attempt_date_time': 'lastAttemptDateTime'
        }

        self._context = context
        self._type = type
        self._activity_id = activity_id
        self._attempts = attempts
        self._last_attempt_date_time = last_attempt_date_time

    @classmethod
    def from_dict(cls, dikt) -> 'ActivityAttemptCounter':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ActivityAttemptCounter of this ActivityAttemptCounter.  # noqa: E501
        :rtype: ActivityAttemptCounter
        """
        return util.deserialize_model(dikt, cls)

    @property
    def context(self) -> str:
        """Gets the context of this ActivityAttemptCounter.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :return: The context of this ActivityAttemptCounter.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context: str):
        """Sets the context of this ActivityAttemptCounter.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :param context: The context of this ActivityAttemptCounter.
        :type context: str
        """
        if context is None:
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def type(self) -> str:
        """Gets the type of this ActivityAttemptCounter.

        The value of this field will always be \"ActivityAttemptCounter\".  # noqa: E501

        :return: The type of this ActivityAttemptCounter.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this ActivityAttemptCounter.

        The value of this field will always be \"ActivityAttemptCounter\".  # noqa: E501

        :param type: The type of this ActivityAttemptCounter.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def activity_id(self) -> str:
        """Gets the activity_id of this ActivityAttemptCounter.

        TODO  # noqa: E501

        :return: The activity_id of this ActivityAttemptCounter.
        :rtype: str
        """
        return self._activity_id

    @activity_id.setter
    def activity_id(self, activity_id: str):
        """Sets the activity_id of this ActivityAttemptCounter.

        TODO  # noqa: E501

        :param activity_id: The activity_id of this ActivityAttemptCounter.
        :type activity_id: str
        """
        if activity_id is None:
            raise ValueError("Invalid value for `activity_id`, must not be `None`")  # noqa: E501

        self._activity_id = activity_id

    @property
    def attempts(self) -> float:
        """Gets the attempts of this ActivityAttemptCounter.

        TODO  # noqa: E501

        :return: The attempts of this ActivityAttemptCounter.
        :rtype: float
        """
        return self._attempts

    @attempts.setter
    def attempts(self, attempts: float):
        """Sets the attempts of this ActivityAttemptCounter.

        TODO  # noqa: E501

        :param attempts: The attempts of this ActivityAttemptCounter.
        :type attempts: float
        """
        if attempts is None:
            raise ValueError("Invalid value for `attempts`, must not be `None`")  # noqa: E501

        self._attempts = attempts

    @property
    def last_attempt_date_time(self) -> datetime:
        """Gets the last_attempt_date_time of this ActivityAttemptCounter.

        TODO  # noqa: E501

        :return: The last_attempt_date_time of this ActivityAttemptCounter.
        :rtype: datetime
        """
        return self._last_attempt_date_time

    @last_attempt_date_time.setter
    def last_attempt_date_time(self, last_attempt_date_time: datetime):
        """Sets the last_attempt_date_time of this ActivityAttemptCounter.

        TODO  # noqa: E501

        :param last_attempt_date_time: The last_attempt_date_time of this ActivityAttemptCounter.
        :type last_attempt_date_time: datetime
        """

        self._last_attempt_date_time = last_attempt_date_time
