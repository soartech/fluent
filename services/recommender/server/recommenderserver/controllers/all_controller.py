from recommenderserver.models.recommendation import Recommendation
from recommenderserver.recommender.recommender import Recommender
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.row_strategies import AllActivities
from recommenderserver.recommender.utils import mongo_id_from_url, load_or_instantiate
from cass_graph_client.cass_graph import CassGraph

def all_get(learnerId):  # noqa: E501
    """Get all activities

    Returns all activities. # noqa: E501

    :param learnerId: Id of the learner to get a recommendation for
    :type learnerId: str

    :rtype: Recommendation
    """
    print("INFO: Received request for all activities recommendation for learner with id {}".format(learnerId))
    query_cacher = QueryCacher()
    learner, etag = query_cacher.get_learner(mongo_id_from_url(learnerId))
    if learner is None:
        return {"error_msg": "Learner cannot be found"}, 404
    print("INFO: Detected goals for learner with id {}. Goals={}".format(learnerId, learner.goals))
    cass_graph = load_or_instantiate('recommenderserver.resources', CassGraph, '603d5ac2-fa9e-43c3-9c50-87ff65804ccd')

    recommendation = Recommender(learner=learner,
                                 etag=etag,
                                 query_cacher=query_cacher,
                                 elo_row_strategy_classes=[],
                                 activity_row_strategy_classes=[AllActivities],
                                 not_enough_content_elo_row_strategy_classes=[],
                                 not_enough_content_activity_row_strategy_classes=[],
                                 min_content_threshold=-1,
                                 cass_graph=cass_graph,
                                 filter_locked=False).get_recommendation()

    print(
        'INFO: All activities recommendation made for learner with id {}. Recommendation: {}'.format(learnerId,
                                                                                               recommendation.to_dict()))
    return recommendation
