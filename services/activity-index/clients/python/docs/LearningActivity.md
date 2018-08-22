# LearningActivity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**about** | **str** | The subject of the content provided by the Learning Activity. | [optional] 
**educational_alignment** | [**list[AlignmentObject]**](AlignmentObject.md) |  | 
**associated_media** | **object** | A media object that encodes this CreativeWork. This property is a synonym for encoding. | [optional] 
**funder** | **object** | A person or organization that supports (sponsors) something through some kind of financial contribution. | [optional] 
**position** | **int** | The position of an item in a series or sequence of items. | [optional] 
**audio** | **object** | An embedded audio object. | [optional] 
**work_example** | **object** | Example/instance/realization/derivation of the concept of this creative work. eg. The paperback edition, first edition, or eBook. | [optional] 
**provider** | [**Organization**](Organization.md) | The provider of the Learning Activity. | 
**encoding** | **object** | A media object that encodes this CreativeWork. This property is a synonym for associatedMedia. | [optional] 
**interactivity_type** | **str** | The predominant mode of learning supported by the learning resource. Acceptable values are active, expositive, or mixed. | 
**accessibility_summary** | **str** | A human-readable summary of specific accessibility features or deficiencies, consistent with the other accessibility metadata but expressing subtleties such as  short descriptions are present but long descriptions will be needed for non-visual users  or  short descriptions are present and no long descriptions are needed.  | [optional] 
**character** | **object** | Fictional person connected with a creative work. | [optional] 
**audience** | **object** | An intended audience, i.e. a group for whom something was created. | [optional] 
**source_organization** | **object** | The Organization on whose behalf the creator was working. | [optional] 
**is_part_of** | **object** | Indicates a CreativeWork that this CreativeWork is (in some sense) part of. | [optional] 
**video** | **object** | An embedded video object. | [optional] 
**publisher** | [**Organization**](Organization.md) | The organization credited with publishing the Learning Activity. | [optional] 
**publication** | **object** | A publication event associated with the item. | [optional] 
**text** | **str** | The textual content of this CreativeWork. | [optional] 
**expires** | **datetime** | Date the content expires and is no longer useful or available. For example a VideoObject or NewsArticle whose availability or relevance is time-limited, or a ClaimReview fact check whose publisher wants to indicate that it may no longer be relevant (or helpful to highlight) after some date. | [optional] 
**contributor** | **object** | A secondary contributor to the CreativeWork or Event. | [optional] 
**reviews** | **object** | Review of the item. | [optional] 
**typical_age_range** | **str** | The typical expected age range, e.g.  7-9 ,  11- . | [optional] 
**released_event** | **object** | The place and time the release was issued, expressed as a PublicationEvent. | [optional] 
**educational_use** | **list[str]** | The purposes of the activity in the context of education. | 
**content_location** | **object** | The location depicted or described in the content. For example, the location in a photograph or painting. | [optional] 
**schema_version** | **str** | Indicates (by URL or string) a particular version of a schema used in some CreativeWork. For example, a document could declare a schemaVersion using an URL such as http://schema.org/version/2.0/ if precise indication of schema version was required by some application. | [optional] 
**accessibility_feature** | **str** | In Schema.org, content features that support accessibility. Used here to list compatible devices. | 
**aggregate_rating** | [**AggregateRating**](AggregateRating.md) | The overall rating, based on a collection of reviews or ratings, of the item. | [optional] 
**alternative_headline** | **str** | A secondary title of the CreativeWork. | [optional] 
**location_created** | **object** | The location where the CreativeWork was created, which may not be the same as the location depicted in the CreativeWork. | [optional] 
**access_mode_sufficient** | **str** | A list of single or combined accessModes that are sufficient to understand all the intellectual content of a resource. Expected values include:  auditory, tactile, textual, visual. | [optional] 
**temporal_coverage** | **datetime** | The temporalCoverage of a CreativeWork indicates the period that the content applies to, i.e. that it describes, either as a DateTime or as a textual string indicating a time period in ISO 8601 time interval format. In       the case of a Dataset it will typically indicate the relevant time period in a precise notation (e.g. for a 2011 census dataset, the year 2011 would be written  2011/2012 ). Other forms of content e.g. ScholarlyArticle, Book, TVSeries or TVEpisode may indicate their temporalCoverage in broader terms - textually or via well-known URL.       Written works such as books may sometimes have precise temporal coverage too, e.g. a work set in 1939 - 1945 can be indicated in ISO 8601 interval format format via  1939/1945 . | [optional] 
**accountable_person** | **object** | Specifies the Person that is legally accountable for the CreativeWork. | [optional] 
**spatial_coverage** | **object** | The spatialCoverage of a CreativeWork indicates the place(s) which are the focus of the content. It is a subproperty of       contentLocation intended primarily for more technical and detailed materials. For example with a Dataset, it indicates       areas that the dataset describes: a dataset of New York weather would have spatialCoverage which was the place: the state of New York. | [optional] 
**offers** | **object** | An offer to provide this item—for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event. | [optional] 
**editor** | **object** | Specifies the Person who edited the CreativeWork. | [optional] 
**discussion_url** | **str** | A link to the page containing the comments of the CreativeWork. | [optional] 
**award** | **str** | An award won by or for this item. | [optional] 
**copyright_holder** | **object** | The party holding the legal copyright to the CreativeWork. | [optional] 
**accessibility_hazard** | **str** | A characteristic of the described resource that is physiologically dangerous to some users. Related to WCAG 2.0 guideline 2.3 (WebSchemas wiki lists possible values). | [optional] 
**copyright_year** | **float** | The year during which the claimed copyright for the CreativeWork was first asserted. | [optional] 
**awards** | **str** | Awards won by or for this item. | [optional] 
**recorded_at** | **object** | The Event where the CreativeWork was recorded. The CreativeWork may capture all or part of the event. | [optional] 
**comment_count** | **int** | The number of comments this CreativeWork (e.g. Article, Question or Answer) has received. This is most applicable to works published in Web sites with commenting system; additional comments may exist elsewhere. | [optional] 
**file_format** | **str** | Media type, typically MIME format (see IANA site) of the content e.g. application/zip of a SoftwareApplication binary. In cases where a CreativeWork has several media type representations,  encoding  can be used to indicate each MediaObject alongside particular fileFormat information. Unregistered or niche file formats can be indicated instead via the most appropriate URL, e.g. defining Web page or a Wikipedia entry. | [optional] 
**in_language** | **object** | The language of the content or performance or used in an action. Please use one of the language codes from the IETF BCP 47 standard. See also availableLanguage. | [optional] 
**accessibility_api** | **str** | In Schema.org, indicates that the resource is compatible with the referenced accessibility API. Used here to list compatible platforms. | [optional] 
**interaction_statistic** | **object** | The number of interactions for the CreativeWork using the WebSite or SoftwareApplication. The most specific child type of InteractionCounter should be used. | [optional] 
**content_rating** | **str** | Official rating of a piece of content—for example, MPAA PG-13 . | [optional] 
**learning_resource_type** | **str** | The predominant type or kind characterizing the learning resource. | 
**access_mode** | **str** | The human sensory perceptual system or cognitive faculty through which a person may process or perceive information. Expected values include: auditory, tactile, textual, visual, colorDependent, chartOnVisual, chemOnVisual, diagramOnVisual, mathOnVisual, musicOnVisual, textOnVisual. | [optional] 
**material** | **str** | A material that something is made from, e.g. leather, wool, cotton, paper. | [optional] 
**is_family_friendly** | **bool** | Indicates whether this content is family friendly. | [optional] 
**example_of_work** | **object** | A creative work that this work is an example/instance/realization/derivation of. | [optional] 
**version** | **str** | The version of the CreativeWork embodied by the Learning Activity. | [optional] 
**date_modified** | **datetime** | The date on which the CreativeWork was most recently modified or when the item s entry was modified within a DataFeed. | [optional] 
**main_entity** | **object** | Indicates the primary entity described in some page or other CreativeWork. | [optional] 
**genre** | **str** | Genre of the creative work, broadcast channel or group. | [optional] 
**keywords** | **str** | Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas. | [optional] 
**author** | [**Person**](Person.md) | The author of the Learning Activity. | [optional] 
**is_based_on_url** | **object** | A resource that was used in the creation of this resource. This term can be repeated for multiple sources. For example, http://example.com/great-multiplication-intro.html. | [optional] 
**time_required** | **str** | Approximate or typical time it takes to work with or through this learning resource for the typical intended target audience. | 
**translator** | **object** | Organization or person who adapts a creative work to different languages, regional differences and technical requirements of a target market, or that translates during some event. | [optional] 
**thumbnail_url** | **str** | A thumbnail image relevant to the Thing. | [optional] 
**has_part** | **object** | Indicates a CreativeWork that is (in some sense) a part of this CreativeWork. | [optional] 
**comment** | **object** | Comments, typically from users. | [optional] 
**review** | **object** | A review of the item. | [optional] 
**license** | **str** | The license of the Learning Activity. | [optional] 
**accessibility_control** | **str** | Identifies input methods that are sufficient to fully control the described resource (WebSchemas wiki lists possible values). | [optional] 
**encodings** | **object** | A media object that encodes this CreativeWork. | [optional] 
**is_based_on** | **object** | A resource that was used in the creation of this resource. This term can be repeated for multiple sources. For example, http://example.com/great-multiplication-intro.html. | [optional] 
**creator** | **object** | The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork. | [optional] 
**publishing_principles** | **object** | The publishingPrinciples property indicates (typically via URL) a document describing the editorial principles of an Organization (or individual e.g. a Person writing a blog) that relate to their activities as a publisher, e.g. ethics or diversity policies. When applied to a CreativeWork (e.g. NewsArticle) the principles are those of the party primarily responsible for the creation of the CreativeWork.  While such policies are most typically expressed in natural language, sometimes related information (e.g. indicating a funder) can be expressed using schema.org terminology. | [optional] 
**sponsor** | **object** | A person or organization that supports a thing through a pledge, promise, or financial contribution. e.g. a sponsor of a Medical Study or a corporate sponsor of an event. | [optional] 
**producer** | **object** | The person or organization who produced the work (e.g. music album, movie, tv/radio series etc.). | [optional] 
**mentions** | **object** | Indicates that the CreativeWork contains a reference to, but is not necessarily about a concept. | [optional] 
**date_created** | **datetime** | The date on which the resource was created. | 
**date_published** | **datetime** | Date of first broadcast/publication. | [optional] 
**is_accessible_for_free** | **bool** | A flag to signal that the item, event, or place is accessible for free. | [optional] 
**headline** | **str** | Headline of the article. | [optional] 
**citation** | **object** | A citation or reference to another creative work, such as another publication, web page, scholarly article, etc. | [optional] 
**same_as** | **str** | URL of a reference Web page that unambiguously indicates the item s identity. E.g. the URL of the item s Wikipedia page, Wikidata entry, or official website. | [optional] 
**url** | **str** | Launch URL to lanuch the learning activity. | 
**image** | **str** | A URL of the activity&#39;s image. | 
**additional_type** | **str** | An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the  typeof  attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally. | [optional] 
**name** | **str** | The title of the Learning Activity. | 
**identifier** | **str** | The URL that identifies the learning activity. For the 2018 prototype, this URL will include the value of the _id field from MongoDB. | 
**potential_action** | **object** | Indicates a potential Action, which describes an idealized action in which this thing would play an  object  role. | [optional] 
**main_entity_of_page** | **str** | Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See background notes for details. | [optional] 
**description** | **str** | A description of the Learning Activity. | 
**disambiguating_description** | **str** | A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation. | [optional] 
**alternate_name** | **str** | An alias for the item. | [optional] 
**context** | **str** | The constant link in this property should return file tla-declarations.jsonld. The value of this field will always be \&quot;https://tla.adl.net/declarations\&quot;. | 
**type** | **str** | The value of this field will always be \&quot;LearningActivity\&quot;. | 
**learning_stage** | **str** | Categories that are used to order the presentation order of activities. | 
**attempt_rate** | **float** | TBD (TODO ASAP) | [optional] 
**additionaltype** | **str** | In Schema.org, an additional type for this item. Used here to contain Launch URL with params included. | [optional] 
**motivation_image** | **str** | An image showing motivation for performing the activity, where you can get to in the future if you learn the basics now. | [optional] 
**content_ur_ls** | **list[str]** | The url for any content that the activity uses such as a video or powerpoint. | [optional] 
**metadata_file** | **str** | Name of the file used to add/update the activity metadata in the Activity Index database. | 
**popularity_rating** | **float** | Population level statistic on whether the activity is found to be popular among learners. | [optional] 
**emotion_rating** | **str** | Population level statistic on which emotion this activity evokes most often in learners. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


