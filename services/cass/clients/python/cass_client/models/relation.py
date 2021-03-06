# coding: utf-8

"""
    CASS API

    This API is used to interact with the data stored in the CASS database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Relation(object):
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
        'id': 'str',
        'owner': 'list[str]',
        'signature': 'list[str]',
        'relation_type': 'str',
        'schemadate_created': 'datetime',
        'source': 'str',
        'target': 'str'
    }

    attribute_map = {
        'context': '@context',
        'type': '@type',
        'id': '@id',
        'owner': '@owner',
        'signature': '@signature',
        'relation_type': 'relationType',
        'schemadate_created': 'schema:dateCreated',
        'source': 'source',
        'target': 'target'
    }

    def __init__(self, context=None, type=None, id=None, owner=None, signature=None, relation_type=None, schemadate_created=None, source=None, target=None):  # noqa: E501
        """Relation - a model defined in Swagger"""  # noqa: E501

        self._context = None
        self._type = None
        self._id = None
        self._owner = None
        self._signature = None
        self._relation_type = None
        self._schemadate_created = None
        self._source = None
        self._target = None
        self.discriminator = None

        if context is not None:
            self.context = context
        if type is not None:
            self.type = type
        if id is not None:
            self.id = id
        if owner is not None:
            self.owner = owner
        if signature is not None:
            self.signature = signature
        if relation_type is not None:
            self.relation_type = relation_type
        if schemadate_created is not None:
            self.schemadate_created = schemadate_created
        if source is not None:
            self.source = source
        if target is not None:
            self.target = target

    @property
    def context(self):
        """Gets the context of this Relation.  # noqa: E501


        :return: The context of this Relation.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this Relation.


        :param context: The context of this Relation.  # noqa: E501
        :type: str
        """
        allowed_values = ["http://insertCassSchemaUrl/0.3"]  # noqa: E501
        if context not in allowed_values:
            raise ValueError(
                "Invalid value for `context` ({0}), must be one of {1}"  # noqa: E501
                .format(context, allowed_values)
            )

        self._context = context

    @property
    def type(self):
        """Gets the type of this Relation.  # noqa: E501


        :return: The type of this Relation.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Relation.


        :param type: The type of this Relation.  # noqa: E501
        :type: str
        """
        allowed_values = ["Relation"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def id(self):
        """Gets the id of this Relation.  # noqa: E501

        The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details.  # noqa: E501

        :return: The id of this Relation.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Relation.

        The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details.  # noqa: E501

        :param id: The id of this Relation.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def owner(self):
        """Gets the owner of this Relation.  # noqa: E501

        Owner public key  # noqa: E501

        :return: The owner of this Relation.  # noqa: E501
        :rtype: list[str]
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Relation.

        Owner public key  # noqa: E501

        :param owner: The owner of this Relation.  # noqa: E501
        :type: list[str]
        """

        self._owner = owner

    @property
    def signature(self):
        """Gets the signature of this Relation.  # noqa: E501

        Owner signature  # noqa: E501

        :return: The signature of this Relation.  # noqa: E501
        :rtype: list[str]
        """
        return self._signature

    @signature.setter
    def signature(self, signature):
        """Sets the signature of this Relation.

        Owner signature  # noqa: E501

        :param signature: The signature of this Relation.  # noqa: E501
        :type: list[str]
        """

        self._signature = signature

    @property
    def relation_type(self):
        """Gets the relation_type of this Relation.  # noqa: E501

        Enumerated string describing the relation. May be: 'narrows', 'desires', 'requires', 'isEnabledBy', 'isRelatedTo', or 'isEquivalentTo'.  # noqa: E501

        :return: The relation_type of this Relation.  # noqa: E501
        :rtype: str
        """
        return self._relation_type

    @relation_type.setter
    def relation_type(self, relation_type):
        """Sets the relation_type of this Relation.

        Enumerated string describing the relation. May be: 'narrows', 'desires', 'requires', 'isEnabledBy', 'isRelatedTo', or 'isEquivalentTo'.  # noqa: E501

        :param relation_type: The relation_type of this Relation.  # noqa: E501
        :type: str
        """
        allowed_values = ["narrows", "requires", "desires", "isEnabledBy", "isRelatedTo", "isEquivalentTo"]  # noqa: E501
        if relation_type not in allowed_values:
            raise ValueError(
                "Invalid value for `relation_type` ({0}), must be one of {1}"  # noqa: E501
                .format(relation_type, allowed_values)
            )

        self._relation_type = relation_type

    @property
    def schemadate_created(self):
        """Gets the schemadate_created of this Relation.  # noqa: E501

        The date the competency was created.  # noqa: E501

        :return: The schemadate_created of this Relation.  # noqa: E501
        :rtype: datetime
        """
        return self._schemadate_created

    @schemadate_created.setter
    def schemadate_created(self, schemadate_created):
        """Sets the schemadate_created of this Relation.

        The date the competency was created.  # noqa: E501

        :param schemadate_created: The schemadate_created of this Relation.  # noqa: E501
        :type: datetime
        """

        self._schemadate_created = schemadate_created

    @property
    def source(self):
        """Gets the source of this Relation.  # noqa: E501

        URL of the competency at the beginning of the relation.  # noqa: E501

        :return: The source of this Relation.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this Relation.

        URL of the competency at the beginning of the relation.  # noqa: E501

        :param source: The source of this Relation.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def target(self):
        """Gets the target of this Relation.  # noqa: E501

        URL of the competency at the end of the relation.  # noqa: E501

        :return: The target of this Relation.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this Relation.

        URL of the competency at the end of the relation.  # noqa: E501

        :param target: The target of this Relation.  # noqa: E501
        :type: str
        """

        self._target = target

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
        if not isinstance(other, Relation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
