# Recommendation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**timestamp** | **datetime** | ISO8601 formatted timestamp | [optional] 
**learner** | **str** | ID of the learner requesting the recommendation | [optional] 
**assignment** | [**RecommendedActivity**](RecommendedActivity.md) |  | [optional] 
**recommendations** | [**list[RecommendationRow]**](RecommendationRow.md) | Array of RecommendationRow objects. Null if assignment is not null. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


