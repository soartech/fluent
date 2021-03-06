# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from learner_inferences_server.models.base_model_ import Model
from learner_inferences_server import util


class MasteryProbability(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, context: str=None, type: str=None, competency_id: str=None, probability: float=None, timestamp: datetime=None, source: str=None):  # noqa: E501
        """MasteryProbability - a model defined in Swagger

        :param context: The context of this MasteryProbability.  # noqa: E501
        :type context: str
        :param type: The type of this MasteryProbability.  # noqa: E501
        :type type: str
        :param competency_id: The competency_id of this MasteryProbability.  # noqa: E501
        :type competency_id: str
        :param probability: The probability of this MasteryProbability.  # noqa: E501
        :type probability: float
        :param timestamp: The timestamp of this MasteryProbability.  # noqa: E501
        :type timestamp: datetime
        :param source: The source of this MasteryProbability.  # noqa: E501
        :type source: str
        """
        self.swagger_types = {
            'context': str,
            'type': str,
            'competency_id': str,
            'probability': float,
            'timestamp': datetime,
            'source': str
        }

        self.attribute_map = {
            'context': '@context',
            'type': '@type',
            'competency_id': 'competencyId',
            'probability': 'probability',
            'timestamp': 'timestamp',
            'source': 'source'
        }

        self._context = context
        self._type = type
        self._competency_id = competency_id
        self._probability = probability
        self._timestamp = timestamp
        self._source = source

    @classmethod
    def from_dict(cls, dikt) -> 'MasteryProbability':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MasteryProbability of this MasteryProbability.  # noqa: E501
        :rtype: MasteryProbability
        """
        return util.deserialize_model(dikt, cls)

    @property
    def context(self) -> str:
        """Gets the context of this MasteryProbability.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :return: The context of this MasteryProbability.
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context: str):
        """Sets the context of this MasteryProbability.

        The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \"https://tla.adl.net/declarations\".  # noqa: E501

        :param context: The context of this MasteryProbability.
        :type context: str
        """
        if context is None:
            raise ValueError("Invalid value for `context`, must not be `None`")  # noqa: E501

        self._context = context

    @property
    def type(self) -> str:
        """Gets the type of this MasteryProbability.

        The value of this field will always be \"MasteryProbability\".  # noqa: E501

        :return: The type of this MasteryProbability.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this MasteryProbability.

        The value of this field will always be \"MasteryProbability\".  # noqa: E501

        :param type: The type of this MasteryProbability.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def competency_id(self) -> str:
        """Gets the competency_id of this MasteryProbability.

        TODO  # noqa: E501

        :return: The competency_id of this MasteryProbability.
        :rtype: str
        """
        return self._competency_id

    @competency_id.setter
    def competency_id(self, competency_id: str):
        """Sets the competency_id of this MasteryProbability.

        TODO  # noqa: E501

        :param competency_id: The competency_id of this MasteryProbability.
        :type competency_id: str
        """
        if competency_id is None:
            raise ValueError("Invalid value for `competency_id`, must not be `None`")  # noqa: E501

        self._competency_id = competency_id

    @property
    def probability(self) -> float:
        """Gets the probability of this MasteryProbability.

        TODO  # noqa: E501

        :return: The probability of this MasteryProbability.
        :rtype: float
        """
        return self._probability

    @probability.setter
    def probability(self, probability: float):
        """Sets the probability of this MasteryProbability.

        TODO  # noqa: E501

        :param probability: The probability of this MasteryProbability.
        :type probability: float
        """
        if probability is None:
            raise ValueError("Invalid value for `probability`, must not be `None`")  # noqa: E501

        self._probability = probability

    @property
    def timestamp(self) -> datetime:
        """Gets the timestamp of this MasteryProbability.

        TODO  # noqa: E501

        :return: The timestamp of this MasteryProbability.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """Sets the timestamp of this MasteryProbability.

        TODO  # noqa: E501

        :param timestamp: The timestamp of this MasteryProbability.
        :type timestamp: datetime
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def source(self) -> str:
        """Gets the source of this MasteryProbability.

        Source of the probability estimate.  # noqa: E501

        :return: The source of this MasteryProbability.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source: str):
        """Sets the source of this MasteryProbability.

        Source of the probability estimate.  # noqa: E501

        :param source: The source of this MasteryProbability.
        :type source: str
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")  # noqa: E501

        self._source = source
