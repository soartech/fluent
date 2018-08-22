# Relation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**id** | **str** | The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See background notes for more details. | [optional] 
**owner** | **list[str]** | Owner public key | [optional] 
**signature** | **list[str]** | Owner signature | [optional] 
**relation_type** | **str** | Enumerated string describing the relation. May be: &#39;narrows&#39;, &#39;desires&#39;, &#39;requires&#39;, &#39;isEnabledBy&#39;, &#39;isRelatedTo&#39;, or &#39;isEquivalentTo&#39;. | [optional] 
**schemadate_created** | **datetime** | The date the competency was created. | [optional] 
**source** | **str** | URL of the competency at the beginning of the relation. | [optional] 
**target** | **str** | URL of the competency at the end of the relation. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


