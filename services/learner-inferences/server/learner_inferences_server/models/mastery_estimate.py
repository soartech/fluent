# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from learner_inferences_server.models.base_model_ import Model
from learner_inferences_server import util


class MasteryEstimate(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, context: str=None, type: str=None, competency_id: str=None, mastery: str=None, timestamp: datetime=None):  # noqa: E501
        """MasteryEstimate - a model defined in Swagger

        :param context: The context of this MasteryEstimate.  # noqa: E501
        :type context: str
        :param type: The type of this MasteryEstimate.  # noqa: E501
        :type type: str
        :param competency_id: The competency_id of this MasteryEstimate.  # noqa: E501
        :type competency_id: str
        :param mastery: The mastery of this MasteryEstimate.  # noqa: E501
        :type mastery: str
        :param timestamp: The timestamp of this MasteryEstimate.  # noqa: E501
        :type timestamp: datetime
        """
        self.swagger_types = {
            'context': str,
            'type': str,
            'competency_id': str,
            'mastery': str,
            'timestamp': datetime
        }

        self.attribute_map = {
            'context': '@context',
            'type': '@type',
            'competency_id': 'competencyId',
            'mastery': 'mastery',
            'timestamp': 'timestamp'
        }

        self._context = context
        self._type = type
        self._competency_id = competency_id
        self._mastery = mastery
        self._timestamp = timestamp

    @classmethod
    def from_dict(cls, dikt) -> 'MasteryEstimate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MasteryEstimate of this MasteryEstimate.  # noqa: E501
        :rtype: MasteryEstimate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def context(self) -> str:
        """Gets the context of this MasteryEstimate.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :return: The context of this MasteryEstimate.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context: str):
        """Sets the context of this MasteryEstimate.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :param context: The context of this MasteryEstimate.
        :type context: str
        """
        if context is None:
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def type(self) -> str:
        """Gets the type of this MasteryEstimate.

        The value of this field will always be \"MasteryEstimate\".  # noqa: E501

        :return: The type of this MasteryEstimate.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this MasteryEstimate.

        The value of this field will always be \"MasteryEstimate\".  # noqa: E501

        :param type: The type of this MasteryEstimate.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def competency_id(self) -> str:
        """Gets the competency_id of this MasteryEstimate.

        TODO  # noqa: E501

        :return: The competency_id of this MasteryEstimate.
        :rtype: str
        """
        return self._competency_id

    @competency_id.setter
    def competency_id(self, competency_id: str):
        """Sets the competency_id of this MasteryEstimate.

        TODO  # noqa: E501

        :param competency_id: The competency_id of this MasteryEstimate.
        :type competency_id: str
        """
        if competency_id is None:
            raise ValueError("Invalid value for `competency_id`, must not be `None`")  # noqa: E501

        self._competency_id = competency_id

    @property
    def mastery(self) -> str:
        """Gets the mastery of this MasteryEstimate.

        TODO  # noqa: E501

        :return: The mastery of this MasteryEstimate.
        :rtype: str
        """
        return self._mastery

    @mastery.setter
    def mastery(self, mastery: str):
        """Sets the mastery of this MasteryEstimate.

        TODO  # noqa: E501

        :param mastery: The mastery of this MasteryEstimate.
        :type mastery: str
        """
        if mastery is None:
            raise ValueError("Invalid value for `mastery`, must not be `None`")  # noqa: E501

        self._mastery = mastery

    @property
    def timestamp(self) -> datetime:
        """Gets the timestamp of this MasteryEstimate.

        TODO  # noqa: E501

        :return: The timestamp of this MasteryEstimate.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """Sets the timestamp of this MasteryEstimate.

        TODO  # noqa: E501

        :param timestamp: The timestamp of this MasteryEstimate.
        :type timestamp: datetime
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp
