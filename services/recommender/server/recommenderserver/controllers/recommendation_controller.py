from recommenderserver.models.recommendation import Recommendation
from recommenderserver.recommender.recommender import Recommender, MandatoryAssignmentMaker
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.utils import mongo_id_from_url, load_or_instantiate, get_aligned_tlo, print_with_time
from cass_graph_client.cass_graph import CassGraph
from recommenderserver.xapi_wrapper import XApiStatement, XAPISender
from recommenderserver.config import Config, LoggingLRSConfig
from recommenderserver.recommender.config import RowStrategyConfig, MandatoryAssignmentMakerConfig

def recommendation_get(learnerId: str, focusedCompetencies=None):  # noqa: E501
    """Get a new recommendation

     # noqa: E501

    :param learnerId: Id of the learner to get a recommendation for
    :type learnerId: str

    :rtype: Recommendation
    """
    print("INFO: Received request for recommendation for learner with id {}".format(learnerId))
    if focusedCompetencies != None:
        print("INFO: Getting recommendations with focused competencies: {}".format(focusedCompetencies))
    else:
        focusedCompetencies = False

    query_cacher = QueryCacher()
    learner, etag = query_cacher.get_learner(mongo_id_from_url(learnerId))
    if learner is None:
        return {"error_msg": "Learner cannot be found"}, 404
    print("INFO: Detected goals for learner with id {}. Goals={}".format(learnerId, learner.goals))
    cass_graph = load_or_instantiate('recommenderserver.resources', CassGraph, '603d5ac2-fa9e-43c3-9c50-87ff65804ccd')

    if MandatoryAssignmentMakerConfig.USE_MANDATORY_ASSIGNMENTS:
        mandatory_assignment_maker = MandatoryAssignmentMaker(learner, etag, query_cacher, cass_graph)
        assignment = mandatory_assignment_maker.get_mandatory_assignment()

        if assignment is not None:
            print(
                'INFO: Mandatory Assignment Recommendation made for learner with id {}. Recommendation: {}'.format(
                    learnerId, assignment.to_dict()))

            assigned_activity = query_cacher.get_activity(assignment.assignment.activity_id)
            aligned_tlo = get_aligned_tlo(assigned_activity)
            # TODO - figure out how to encode user's information into this xAPI statement. Likely either in context or result.
            log_statement = XApiStatement(agent_name="Recommender",
                                          agent_url_id=Config.RECOMMENDER_URL,
                                          verb_id="https://w3id.org/xapi/dod-isd/verbs/assigned",
                                          activity_id=aligned_tlo)

            xapi_sender = XAPISender(base_url='http://'+LoggingLRSConfig.BASE_URL,
                                     x_experience_version=LoggingLRSConfig.X_EXPERIENCE_VERSION,
                                     basic_auth_user=LoggingLRSConfig.CLIENT_USR,
                                     basic_auth_pwd=LoggingLRSConfig.CLIENT_PWD)
            if False:
                xapi_sender.statements_post([log_statement])

            return assignment

    recommendation = Recommender(learner=learner,
                                 etag=etag,
                                 query_cacher=query_cacher,
                                 elo_row_strategy_classes=RowStrategyConfig.PRIORITY_COMPETENCY_ROW_STRATEGIES,
                                 activity_row_strategy_classes=RowStrategyConfig.PRIORITY_ACTIVITY_ROW_STRATEGIES,
                                 not_enough_content_elo_row_strategy_classes=RowStrategyConfig.NOT_ENOUGH_CONTENT_ELO_ROW_STRATEGIES,
                                 not_enough_content_activity_row_strategy_classes=[],
                                 cass_graph=cass_graph,
                                 min_content_threshold=-1,
                                 filter_locked=RowStrategyConfig.FILTER_LOCKED_ACTIVITIES,
                                 use_prerequisties=True,
                                 focus_competencies=focusedCompetencies).get_recommendation()

    print_with_time(
        'INFO: Recommendation made for learner with id {}.'.format(learnerId))
    return recommendation
