from recommenderserver.models.recommendation import Recommendation
from recommenderserver.recommender.config import RowStrategyConfig
from recommenderserver.recommender.recommender import Recommender
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.utils import mongo_id_from_url, load_or_instantiate, print_with_time
from cass_graph_client.cass_graph import CassGraph


def upcoming_get(learnerId):  # noqa: E501
    """Get upcoming activities

    Returns an overview of what the learner will be working on (and reflected in upcoming recommendations). It should include current ELO in the sequence that the learner has not yet mastered that they will continue learning. It will also include any ELOs that the learner has forgotten that will be reviewed. # noqa: E501

    :param learnerId: Id of the learner to get a recommendation for
    :type learnerId: str

    :rtype: Recommendation
    """
    print("INFO: Received request for upcoming recommendation for learner with id {}".format(learnerId))
    query_cacher = QueryCacher()
    learner, etag = query_cacher.get_learner(mongo_id_from_url(learnerId))
    if learner is None:
        return {"error_msg": "Learner cannot be found"}, 404
    print("INFO: Detected goals for learner with id {}. Goals={}".format(learnerId, learner.goals))
    cass_graph = load_or_instantiate('recommenderserver.resources', CassGraph, '603d5ac2-fa9e-43c3-9c50-87ff65804ccd')

    recommendation = Recommender(learner=learner,
                                 etag=etag,
                                 query_cacher=query_cacher,
                                 elo_row_strategy_classes=RowStrategyConfig.UPCOMING_COMPETENCY_ROW_STRATEGIES,
                                 activity_row_strategy_classes=[],
                                 not_enough_content_elo_row_strategy_classes=RowStrategyConfig.NOT_ENOUGH_CONTENT_ELO_ROW_STRATEGIES,
                                 not_enough_content_activity_row_strategy_classes=[],
                                 cass_graph=cass_graph,
                                 min_content_threshold=-1,
                                 filter_locked=RowStrategyConfig.FILTER_LOCKED_ACTIVITIES,
                                 use_prerequisties=False).get_recommendation()
    print_with_time(
        'INFO: Upcoming recommendation made for learner with id {}.'.format(learnerId))
    return recommendation
