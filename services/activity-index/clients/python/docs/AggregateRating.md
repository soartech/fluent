# AggregateRating

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_reviewed** | **object** | The item that is being reviewed/rated. | [optional] 
**review_count** | **int** | The count of total number of reviews. | [optional] 
**rating_count** | **int** | The count of total number of ratings. | [optional] 
**rating_value** | **float** | The rating for the content. | [optional] 
**best_rating** | **str** | The highest value allowed in this rating system. If bestRating is omitted, 5 is assumed. | [optional] 
**author** | **object** | The author of this content or rating. Please note that author is special in that HTML 5 provides a special mechanism for indicating authorship via the rel tag. That is equivalent to this and may be used interchangeably. | [optional] 
**worst_rating** | **str** | The lowest value allowed in this rating system. If worstRating is omitted, 1 is assumed. | [optional] 
**same_as** | **str** | URL of a reference Web page that unambiguously indicates the item s identity. E.g. the URL of the item s Wikipedia page, Wikidata entry, or official website. | [optional] 
**url** | **str** | URL of the item. | [optional] 
**image** | **object** | An image of the item. This can be a URL or a fully described ImageObject. | [optional] 
**additional_type** | **str** | An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the  typeof  attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally. | [optional] 
**name** | **str** | The name of the item. | [optional] 
**identifier** | **str** | The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details. | [optional] 
**potential_action** | **object** | Indicates a potential Action, which describes an idealized action in which this thing would play an  object  role. | [optional] 
**main_entity_of_page** | **str** | Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See background notes for details. | [optional] 
**description** | **str** | A description of the item. | [optional] 
**disambiguating_description** | **str** | A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation. | [optional] 
**alternate_name** | **str** | An alias for the item. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

