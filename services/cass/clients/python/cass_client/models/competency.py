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


class Competency(object):
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
        'ceasncoded_notation': 'str',
        'ceasnconcept_term': 'str',
        'dctermstype': 'str',
        'description': 'str',
        'name': 'str',
        'schemadate_created': 'datetime',
        'schemadate_modified': 'datetime'
    }

    attribute_map = {
        'context': '@context',
        'type': '@type',
        'id': '@id',
        'owner': '@owner',
        'signature': '@signature',
        'ceasncoded_notation': 'ceasn:codedNotation',
        'ceasnconcept_term': 'ceasn:conceptTerm',
        'dctermstype': 'dcterms:type',
        'description': 'description',
        'name': 'name',
        'schemadate_created': 'schema:dateCreated',
        'schemadate_modified': 'schema:dateModified'
    }

    def __init__(self, context=None, type=None, id=None, owner=None, signature=None, ceasncoded_notation=None, ceasnconcept_term=None, dctermstype=None, description=None, name=None, schemadate_created=None, schemadate_modified=None):  # noqa: E501
        """Competency - a model defined in Swagger"""  # noqa: E501

        self._context = None
        self._type = None
        self._id = None
        self._owner = None
        self._signature = None
        self._ceasncoded_notation = None
        self._ceasnconcept_term = None
        self._dctermstype = None
        self._description = None
        self._name = None
        self._schemadate_created = None
        self._schemadate_modified = None
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
        if ceasncoded_notation is not None:
            self.ceasncoded_notation = ceasncoded_notation
        if ceasnconcept_term is not None:
            self.ceasnconcept_term = ceasnconcept_term
        if dctermstype is not None:
            self.dctermstype = dctermstype
        if description is not None:
            self.description = description
        if name is not None:
            self.name = name
        if schemadate_created is not None:
            self.schemadate_created = schemadate_created
        if schemadate_modified is not None:
            self.schemadate_modified = schemadate_modified

    @property
    def context(self):
        """Gets the context of this Competency.  # noqa: E501


        :return: The context of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this Competency.


        :param context: The context of this Competency.  # noqa: E501
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
        """Gets the type of this Competency.  # noqa: E501


        :return: The type of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Competency.


        :param type: The type of this Competency.  # noqa: E501
        :type: str
        """
        allowed_values = ["Competency"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def id(self):
        """Gets the id of this Competency.  # noqa: E501

        The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details.  # noqa: E501

        :return: The id of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Competency.

        The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details.  # noqa: E501

        :param id: The id of this Competency.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def owner(self):
        """Gets the owner of this Competency.  # noqa: E501

        Owner public key  # noqa: E501

        :return: The owner of this Competency.  # noqa: E501
        :rtype: list[str]
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Competency.

        Owner public key  # noqa: E501

        :param owner: The owner of this Competency.  # noqa: E501
        :type: list[str]
        """

        self._owner = owner

    @property
    def signature(self):
        """Gets the signature of this Competency.  # noqa: E501

        Owner signature  # noqa: E501

        :return: The signature of this Competency.  # noqa: E501
        :rtype: list[str]
        """
        return self._signature

    @signature.setter
    def signature(self, signature):
        """Sets the signature of this Competency.

        Owner signature  # noqa: E501

        :param signature: The signature of this Competency.  # noqa: E501
        :type: list[str]
        """

        self._signature = signature

    @property
    def ceasncoded_notation(self):
        """Gets the ceasncoded_notation of this Competency.  # noqa: E501

        Chapter-style coded notation for the ELOs and TLOs, e.g. 3.1, 3.2, 3.3, etc...  # noqa: E501

        :return: The ceasncoded_notation of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._ceasncoded_notation

    @ceasncoded_notation.setter
    def ceasncoded_notation(self, ceasncoded_notation):
        """Sets the ceasncoded_notation of this Competency.

        Chapter-style coded notation for the ELOs and TLOs, e.g. 3.1, 3.2, 3.3, etc...  # noqa: E501

        :param ceasncoded_notation: The ceasncoded_notation of this Competency.  # noqa: E501
        :type: str
        """

        self._ceasncoded_notation = ceasncoded_notation

    @property
    def ceasnconcept_term(self):
        """Gets the ceasnconcept_term of this Competency.  # noqa: E501

        The URI ID of the ceasn:conceptTerm used to detrmine if the ELO/TLO is 'Well defined' or 'Ill defined'  # noqa: E501

        :return: The ceasnconcept_term of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._ceasnconcept_term

    @ceasnconcept_term.setter
    def ceasnconcept_term(self, ceasnconcept_term):
        """Sets the ceasnconcept_term of this Competency.

        The URI ID of the ceasn:conceptTerm used to detrmine if the ELO/TLO is 'Well defined' or 'Ill defined'  # noqa: E501

        :param ceasnconcept_term: The ceasnconcept_term of this Competency.  # noqa: E501
        :type: str
        """

        self._ceasnconcept_term = ceasnconcept_term

    @property
    def dctermstype(self):
        """Gets the dctermstype of this Competency.  # noqa: E501

        Determines the type of the competency.  # noqa: E501

        :return: The dctermstype of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._dctermstype

    @dctermstype.setter
    def dctermstype(self, dctermstype):
        """Sets the dctermstype of this Competency.

        Determines the type of the competency.  # noqa: E501

        :param dctermstype: The dctermstype of this Competency.  # noqa: E501
        :type: str
        """

        self._dctermstype = dctermstype

    @property
    def description(self):
        """Gets the description of this Competency.  # noqa: E501

        The description of the competency.  # noqa: E501

        :return: The description of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Competency.

        The description of the competency.  # noqa: E501

        :param description: The description of this Competency.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def name(self):
        """Gets the name of this Competency.  # noqa: E501

        The name of the competency.  # noqa: E501

        :return: The name of this Competency.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Competency.

        The name of the competency.  # noqa: E501

        :param name: The name of this Competency.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def schemadate_created(self):
        """Gets the schemadate_created of this Competency.  # noqa: E501

        The date the competency was created.  # noqa: E501

        :return: The schemadate_created of this Competency.  # noqa: E501
        :rtype: datetime
        """
        return self._schemadate_created

    @schemadate_created.setter
    def schemadate_created(self, schemadate_created):
        """Sets the schemadate_created of this Competency.

        The date the competency was created.  # noqa: E501

        :param schemadate_created: The schemadate_created of this Competency.  # noqa: E501
        :type: datetime
        """

        self._schemadate_created = schemadate_created

    @property
    def schemadate_modified(self):
        """Gets the schemadate_modified of this Competency.  # noqa: E501

        The last time the competency was modified.  # noqa: E501

        :return: The schemadate_modified of this Competency.  # noqa: E501
        :rtype: datetime
        """
        return self._schemadate_modified

    @schemadate_modified.setter
    def schemadate_modified(self, schemadate_modified):
        """Sets the schemadate_modified of this Competency.

        The last time the competency was modified.  # noqa: E501

        :param schemadate_modified: The schemadate_modified of this Competency.  # noqa: E501
        :type: datetime
        """

        self._schemadate_modified = schemadate_modified

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
        if not isinstance(other, Competency):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
