# coding: utf-8

"""
    Asset API

    This API is used to interact with the data stored in the TLA Activity Index database.  # noqa: E501

    OpenAPI spec version: 0.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class AggregateRating(object):
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
        'item_reviewed': 'object',
        'review_count': 'int',
        'rating_count': 'int',
        'rating_value': 'float',
        'best_rating': 'str',
        'author': 'object',
        'worst_rating': 'str',
        'same_as': 'str',
        'url': 'str',
        'image': 'object',
        'additional_type': 'str',
        'name': 'str',
        'identifier': 'str',
        'potential_action': 'object',
        'main_entity_of_page': 'str',
        'description': 'str',
        'disambiguating_description': 'str',
        'alternate_name': 'str'
    }

    attribute_map = {
        'item_reviewed': 'itemReviewed',
        'review_count': 'reviewCount',
        'rating_count': 'ratingCount',
        'rating_value': 'ratingValue',
        'best_rating': 'bestRating',
        'author': 'author',
        'worst_rating': 'worstRating',
        'same_as': 'sameAs',
        'url': 'url',
        'image': 'image',
        'additional_type': 'additionalType',
        'name': 'name',
        'identifier': 'identifier',
        'potential_action': 'potentialAction',
        'main_entity_of_page': 'mainEntityOfPage',
        'description': 'description',
        'disambiguating_description': 'disambiguatingDescription',
        'alternate_name': 'alternateName'
    }

    def __init__(self, item_reviewed=None, review_count=None, rating_count=None, rating_value=None, best_rating=None, author=None, worst_rating=None, same_as=None, url=None, image=None, additional_type=None, name=None, identifier=None, potential_action=None, main_entity_of_page=None, description=None, disambiguating_description=None, alternate_name=None):  # noqa: E501
        """AggregateRating - a model defined in Swagger"""  # noqa: E501

        self._item_reviewed = None
        self._review_count = None
        self._rating_count = None
        self._rating_value = None
        self._best_rating = None
        self._author = None
        self._worst_rating = None
        self._same_as = None
        self._url = None
        self._image = None
        self._additional_type = None
        self._name = None
        self._identifier = None
        self._potential_action = None
        self._main_entity_of_page = None
        self._description = None
        self._disambiguating_description = None
        self._alternate_name = None
        self.discriminator = None

        if item_reviewed is not None:
            self.item_reviewed = item_reviewed
        if review_count is not None:
            self.review_count = review_count
        if rating_count is not None:
            self.rating_count = rating_count
        if rating_value is not None:
            self.rating_value = rating_value
        if best_rating is not None:
            self.best_rating = best_rating
        if author is not None:
            self.author = author
        if worst_rating is not None:
            self.worst_rating = worst_rating
        if same_as is not None:
            self.same_as = same_as
        if url is not None:
            self.url = url
        if image is not None:
            self.image = image
        if additional_type is not None:
            self.additional_type = additional_type
        if name is not None:
            self.name = name
        if identifier is not None:
            self.identifier = identifier
        if potential_action is not None:
            self.potential_action = potential_action
        if main_entity_of_page is not None:
            self.main_entity_of_page = main_entity_of_page
        if description is not None:
            self.description = description
        if disambiguating_description is not None:
            self.disambiguating_description = disambiguating_description
        if alternate_name is not None:
            self.alternate_name = alternate_name

    @property
    def item_reviewed(self):
        """Gets the item_reviewed of this AggregateRating.  # noqa: E501

        The item that is being reviewed/rated.  # noqa: E501

        :return: The item_reviewed of this AggregateRating.  # noqa: E501
        :rtype: object
        """
        return self._item_reviewed

    @item_reviewed.setter
    def item_reviewed(self, item_reviewed):
        """Sets the item_reviewed of this AggregateRating.

        The item that is being reviewed/rated.  # noqa: E501

        :param item_reviewed: The item_reviewed of this AggregateRating.  # noqa: E501
        :type: object
        """

        self._item_reviewed = item_reviewed

    @property
    def review_count(self):
        """Gets the review_count of this AggregateRating.  # noqa: E501

        The count of total number of reviews.  # noqa: E501

        :return: The review_count of this AggregateRating.  # noqa: E501
        :rtype: int
        """
        return self._review_count

    @review_count.setter
    def review_count(self, review_count):
        """Sets the review_count of this AggregateRating.

        The count of total number of reviews.  # noqa: E501

        :param review_count: The review_count of this AggregateRating.  # noqa: E501
        :type: int
        """

        self._review_count = review_count

    @property
    def rating_count(self):
        """Gets the rating_count of this AggregateRating.  # noqa: E501

        The count of total number of ratings.  # noqa: E501

        :return: The rating_count of this AggregateRating.  # noqa: E501
        :rtype: int
        """
        return self._rating_count

    @rating_count.setter
    def rating_count(self, rating_count):
        """Sets the rating_count of this AggregateRating.

        The count of total number of ratings.  # noqa: E501

        :param rating_count: The rating_count of this AggregateRating.  # noqa: E501
        :type: int
        """

        self._rating_count = rating_count

    @property
    def rating_value(self):
        """Gets the rating_value of this AggregateRating.  # noqa: E501

        The rating for the content.  # noqa: E501

        :return: The rating_value of this AggregateRating.  # noqa: E501
        :rtype: float
        """
        return self._rating_value

    @rating_value.setter
    def rating_value(self, rating_value):
        """Sets the rating_value of this AggregateRating.

        The rating for the content.  # noqa: E501

        :param rating_value: The rating_value of this AggregateRating.  # noqa: E501
        :type: float
        """

        self._rating_value = rating_value

    @property
    def best_rating(self):
        """Gets the best_rating of this AggregateRating.  # noqa: E501

        The highest value allowed in this rating system. If bestRating is omitted, 5 is assumed.  # noqa: E501

        :return: The best_rating of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._best_rating

    @best_rating.setter
    def best_rating(self, best_rating):
        """Sets the best_rating of this AggregateRating.

        The highest value allowed in this rating system. If bestRating is omitted, 5 is assumed.  # noqa: E501

        :param best_rating: The best_rating of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._best_rating = best_rating

    @property
    def author(self):
        """Gets the author of this AggregateRating.  # noqa: E501

        The author of this content or rating. Please note that author is special in that HTML 5 provides a special mechanism for indicating authorship via the rel tag. That is equivalent to this and may be used interchangeably.  # noqa: E501

        :return: The author of this AggregateRating.  # noqa: E501
        :rtype: object
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this AggregateRating.

        The author of this content or rating. Please note that author is special in that HTML 5 provides a special mechanism for indicating authorship via the rel tag. That is equivalent to this and may be used interchangeably.  # noqa: E501

        :param author: The author of this AggregateRating.  # noqa: E501
        :type: object
        """

        self._author = author

    @property
    def worst_rating(self):
        """Gets the worst_rating of this AggregateRating.  # noqa: E501

        The lowest value allowed in this rating system. If worstRating is omitted, 1 is assumed.  # noqa: E501

        :return: The worst_rating of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._worst_rating

    @worst_rating.setter
    def worst_rating(self, worst_rating):
        """Sets the worst_rating of this AggregateRating.

        The lowest value allowed in this rating system. If worstRating is omitted, 1 is assumed.  # noqa: E501

        :param worst_rating: The worst_rating of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._worst_rating = worst_rating

    @property
    def same_as(self):
        """Gets the same_as of this AggregateRating.  # noqa: E501

        URL of a reference Web page that unambiguously indicates the item s identity. E.g. the URL of the item s Wikipedia page, Wikidata entry, or official website.  # noqa: E501

        :return: The same_as of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._same_as

    @same_as.setter
    def same_as(self, same_as):
        """Sets the same_as of this AggregateRating.

        URL of a reference Web page that unambiguously indicates the item s identity. E.g. the URL of the item s Wikipedia page, Wikidata entry, or official website.  # noqa: E501

        :param same_as: The same_as of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._same_as = same_as

    @property
    def url(self):
        """Gets the url of this AggregateRating.  # noqa: E501

        URL of the item.  # noqa: E501

        :return: The url of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this AggregateRating.

        URL of the item.  # noqa: E501

        :param url: The url of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def image(self):
        """Gets the image of this AggregateRating.  # noqa: E501

        An image of the item. This can be a URL or a fully described ImageObject.  # noqa: E501

        :return: The image of this AggregateRating.  # noqa: E501
        :rtype: object
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this AggregateRating.

        An image of the item. This can be a URL or a fully described ImageObject.  # noqa: E501

        :param image: The image of this AggregateRating.  # noqa: E501
        :type: object
        """

        self._image = image

    @property
    def additional_type(self):
        """Gets the additional_type of this AggregateRating.  # noqa: E501

        An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the  typeof  attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally.  # noqa: E501

        :return: The additional_type of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._additional_type

    @additional_type.setter
    def additional_type(self, additional_type):
        """Sets the additional_type of this AggregateRating.

        An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the  typeof  attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally.  # noqa: E501

        :param additional_type: The additional_type of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._additional_type = additional_type

    @property
    def name(self):
        """Gets the name of this AggregateRating.  # noqa: E501

        The name of the item.  # noqa: E501

        :return: The name of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AggregateRating.

        The name of the item.  # noqa: E501

        :param name: The name of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def identifier(self):
        """Gets the identifier of this AggregateRating.  # noqa: E501

        The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details.  # noqa: E501

        :return: The identifier of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this AggregateRating.

        The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details.  # noqa: E501

        :param identifier: The identifier of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def potential_action(self):
        """Gets the potential_action of this AggregateRating.  # noqa: E501

        Indicates a potential Action, which describes an idealized action in which this thing would play an  object  role.  # noqa: E501

        :return: The potential_action of this AggregateRating.  # noqa: E501
        :rtype: object
        """
        return self._potential_action

    @potential_action.setter
    def potential_action(self, potential_action):
        """Sets the potential_action of this AggregateRating.

        Indicates a potential Action, which describes an idealized action in which this thing would play an  object  role.  # noqa: E501

        :param potential_action: The potential_action of this AggregateRating.  # noqa: E501
        :type: object
        """

        self._potential_action = potential_action

    @property
    def main_entity_of_page(self):
        """Gets the main_entity_of_page of this AggregateRating.  # noqa: E501

        Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See background notes for details.  # noqa: E501

        :return: The main_entity_of_page of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._main_entity_of_page

    @main_entity_of_page.setter
    def main_entity_of_page(self, main_entity_of_page):
        """Sets the main_entity_of_page of this AggregateRating.

        Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See background notes for details.  # noqa: E501

        :param main_entity_of_page: The main_entity_of_page of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._main_entity_of_page = main_entity_of_page

    @property
    def description(self):
        """Gets the description of this AggregateRating.  # noqa: E501

        A description of the item.  # noqa: E501

        :return: The description of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AggregateRating.

        A description of the item.  # noqa: E501

        :param description: The description of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def disambiguating_description(self):
        """Gets the disambiguating_description of this AggregateRating.  # noqa: E501

        A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation.  # noqa: E501

        :return: The disambiguating_description of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._disambiguating_description

    @disambiguating_description.setter
    def disambiguating_description(self, disambiguating_description):
        """Sets the disambiguating_description of this AggregateRating.

        A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation.  # noqa: E501

        :param disambiguating_description: The disambiguating_description of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._disambiguating_description = disambiguating_description

    @property
    def alternate_name(self):
        """Gets the alternate_name of this AggregateRating.  # noqa: E501

        An alias for the item.  # noqa: E501

        :return: The alternate_name of this AggregateRating.  # noqa: E501
        :rtype: str
        """
        return self._alternate_name

    @alternate_name.setter
    def alternate_name(self, alternate_name):
        """Sets the alternate_name of this AggregateRating.

        An alias for the item.  # noqa: E501

        :param alternate_name: The alternate_name of this AggregateRating.  # noqa: E501
        :type: str
        """

        self._alternate_name = alternate_name

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
        if not isinstance(other, AggregateRating):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other