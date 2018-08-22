from typing import List, Optional

import activity_index_client
import learner_inferences_client
from activity_index_client import LearningActivity
from learner_inferences_client import Learner
from recommenderserver import config
from recommenderserver.recommender.decorators import memoize
from recommenderuisupportclient import LearnerTokens
from recommenderuisupportclient import TokensApi

FILTER_DEBUG_ACTIVITIES = True
FILTER_PRETEST_ACTIVITIES = True
FILTER_POSTTEST_ACTIVITIES = True
FILTER_PLACEHOLDER_ACTIVITIES = True
FILTER_ASSESSMENT_ACTIVITIES = False
FILTER_OLD_ACTIVITIES = True

class QueryCacher(object):
    """
    This class is used to cache the result of network calls made by the recommender and it's constituents.
    """

    def __init__(self,
                 single_activity_api=config.Config.SINGLE_ACTIVITY_API,
                 multiple_activities_api=config.Config.MULTIPLE_ACTIVITIES_API,
                 learner_inferences_url=config.Config.LEARNER_INFERENCE_BASE_URL,
                 token_url=config.Config.RECOMMENDER_UI_SUPPORT_URL,
                 filter_debug=FILTER_DEBUG_ACTIVITIES,
                 filter_pretest=FILTER_PRETEST_ACTIVITIES,
                 filter_posttest=FILTER_POSTTEST_ACTIVITIES,
                 filter_placeholder=FILTER_PLACEHOLDER_ACTIVITIES,
                 filter_assessment=FILTER_ASSESSMENT_ACTIVITIES,
                 filter_old=FILTER_OLD_ACTIVITIES
                 ):
        self.filter_debug = filter_debug
        self.filter_pretest = filter_pretest
        self.filter_posttest = filter_posttest
        self.filter_placeholder = filter_placeholder
        self.filter_assessment = filter_assessment
        self.filter_old = filter_old

        self.multiple_activities_api = multiple_activities_api
        self.single_activity_api = single_activity_api

        self.multiple_learners_api = learner_inferences_client.MultipleLearnersApi()
        self.multiple_learners_api.api_client.configuration.host = learner_inferences_url

        self.single_learner_api = learner_inferences_client.SingleLearnerApi()
        self.single_learner_api.api_client.configuration.host = learner_inferences_url

        self.tokens_api = TokensApi()
        self.tokens_api.api_client.configuration.host = token_url

    def get_activity(self, mongo_activity_id) -> Optional[LearningActivity]:
        try:
            response = self.single_activity_api.get_activity(mongo_activity_id)
            return response
        except:
            return None

    @memoize
    def get_learner(self, learnerId) -> Optional[Learner]:
        try:
            learner, _, response_headers = self.single_learner_api.get_learner_with_http_info(learnerId)
            return learner, response_headers['ETag']
        except Exception as e:
            print("WARN: Exception: {}".format(e))
            return None, None

    def get_activities(self, limit=99999999, offset=0) -> List[LearningActivity]:
        activities = self.multiple_activities_api.get_activities(limit=limit, offset=offset)
        ed_use_to_filter = list()
        from recommenderserver.recommender.utils import MagicStrings
        if self.filter_debug:
            ed_use_to_filter.append(MagicStrings.EducationalUses.DEBUG)
        if self.filter_pretest:
            ed_use_to_filter.append(MagicStrings.EducationalUses.PRE_TEST)
        if self.filter_posttest:
            ed_use_to_filter.append(MagicStrings.EducationalUses.POST_TEST)
        if self.filter_placeholder:
            ed_use_to_filter.append(MagicStrings.EducationalUses.PLACEHOLDER)
        if self.filter_old:
            ed_use_to_filter.append(MagicStrings.EducationalUses.OLD)

        if len(ed_use_to_filter) > 0:
            activities = [
                activity for activity in activities
                if not bool(set(ed_use_to_filter) & set(activity.educational_use))
            ]

        if self.filter_assessment:
            from recommenderserver.recommender.utils import is_assessment
            activities = [
                activity for activity in activities if not is_assessment(activity)
            ]

        return activities

    @memoize
    def get_learner_tokens(self, learnerId) -> Optional[LearnerTokens]:
        try:
            return self.tokens_api.get_learner_tokens(learnerId)
        except:
            return None

    def update_learner(self, identifier, etag, learner_patch):
        self.single_learner_api.update_learner(identifier, etag, learner_obj=learner_patch)

    def get_self_report(self) -> Optional[LearningActivity]:
        all_activities = self.get_activities()
        for activity in all_activities:
            from recommenderserver.recommender.utils import MagicStrings
            if MagicStrings.EducationalUses.SELF_REPORT in activity.educational_use:
                return activity
        return None

    def get_activities_for_elo(self, elo_id: str) -> List[LearningActivity]:
        from recommenderserver.recommender.utils import elo_in_activity
        return [activity for activity in self.get_activities() if elo_in_activity(elo_id, activity)]
