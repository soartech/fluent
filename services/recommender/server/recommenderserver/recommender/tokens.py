from typing import List, Optional
from datetime import datetime, timedelta, timezone
import dateutil.parser
import isodate
from random import randint

from activity_index_client import LearningActivity
from learner_inferences_client import Learner
from recommenderserver.recommender.query_cacher import QueryCacher
from recommenderserver.recommender.utils import get_aligned_elo, get_elo_mastery_estimate, mongo_id_from_url, get_last_activity_url_identifier, MagicStrings, has_challenge_level, has_learner_seen_activity, educational_use_in_activity
from recommenderserver.config import TokenConfig

class Tokens(object):
    def __init__(self, learner: Learner, activity: LearningActivity, query_cacher: QueryCacher):
        self.learner = learner
        self.activity = activity
        self.query_cacher = query_cacher

    @property
    def LOW_REWARD(self):
        return 1

    @property
    def MEDIUM_REWARD(self):
        return 3

    @property
    def LOW_RAND_REWARD(self):
        return randint(1, 3)

    @property
    def MED_RAND_REWARD(self):
        return randint(2, 5)

    @property
    def HIGH_RAND_REWARD(self):
        return randint(5, 10)

    @property
    def LOW_RAND_OPTIONAL_REWARD(self):
        return randint(0, 3)

    @property
    def MED_RAND_OPTIONAL_REWARD(self):
        return randint(0, 5)

    def get_activity_tokens(self):
        elo_id = get_aligned_elo(self.activity)
        mastery_estimate = get_elo_mastery_estimate(elo_id, self.learner)
        # TODO - Figure out better way around this
        try:
            last_activity = self.query_cacher.get_activity(mongo_id_from_url(get_last_activity_url_identifier(self.learner)))
        except:
            last_activity = None

        if TokenConfig.ADVANCED_TOKEN_DECIDER:
            lb_tokens = self.learner_behavior_tokens(self.activity, mastery_estimate, last_activity)
            am_tokens = self.activity_metadata_tokens(elo_id, self.activity)
            history_multiplier = self.learner_activity_history_multiplier(self.learner, self.activity)
            return int(round((lb_tokens + am_tokens)*history_multiplier, 0))
        else:
            return self.simple_token_decider()

    def learner_behavior_tokens(self, activity: LearningActivity, mastery_estimate: str, last_activity: Optional[LearningActivity]):
        point_sum = 0
        if educational_use_in_activity(activity, MagicStrings.EducationalUses.ASSESSES):
            if mastery_estimate == MagicStrings.MasteryEstimates.NOT_HELD:
                point_sum += self.LOW_REWARD
            elif mastery_estimate == MagicStrings.MasteryEstimates.FORGOT:
                point_sum += self.MED_RAND_REWARD
        else:
            if has_learner_seen_activity(self.learner, activity):
                point_sum += self.HIGH_RAND_REWARD
            else:
                if mastery_estimate == MagicStrings.MasteryEstimates.FORGOT:
                    point_sum += self.MEDIUM_REWARD

        # Last activity completed was hard
        if last_activity is not None:
            last_elo = get_aligned_elo(last_activity)
            if has_challenge_level(last_elo, activity, MagicStrings.ChallengeLevels.COMPLEX):
                point_sum += self.LOW_RAND_OPTIONAL_REWARD

        return point_sum

    def activity_metadata_tokens(self, elo: str, activity: LearningActivity):
        point_sum = 0
        if educational_use_in_activity(activity, MagicStrings.EducationalUses.MORE_CONTENT):
            point_sum += self.MED_RAND_REWARD
        elif educational_use_in_activity(activity, MagicStrings.EducationalUses.REFERENCE):
            point_sum += self.LOW_RAND_REWARD

        if has_challenge_level(elo, activity, MagicStrings.ChallengeLevels.COMPLEX):
            point_sum += self.MED_RAND_REWARD
        elif has_challenge_level(elo, activity, MagicStrings.ChallengeLevels.MODERATE):
            point_sum += self.LOW_RAND_REWARD

        if activity.interactivity_type == MagicStrings.InteractivityTypes.PASSIVE:
            point_sum += self.MED_RAND_OPTIONAL_REWARD
        elif activity.interactivity_type == MagicStrings.InteractivityTypes.LIMITED_PARTICIPATION:
            point_sum += self.LOW_RAND_OPTIONAL_REWARD

        if timedelta(minutes=10) < isodate.parse_duration(activity.time_required) < timedelta(minutes=30):
            point_sum += self.LOW_RAND_OPTIONAL_REWARD
        elif isodate.parse_duration(activity.time_required) > timedelta(minutes=30):
            point_sum += self.MED_RAND_OPTIONAL_REWARD

        return point_sum

    def learner_activity_history_multiplier(self, learner: Learner, activity: LearningActivity):
        for attempt in learner.activity_attempt_counters:
            if attempt.activity_id == activity.identifier:
                attempt_time = attempt.last_attempt_date_time
                now = datetime.utcnow().replace(tzinfo=timezone.utc)
                if (now - timedelta(minutes=30)) < attempt_time  and attempt_time < (now - timedelta(minutes=10)):
                    return 0.25
                elif (now - timedelta(minutes=10)) < attempt_time and attempt_time < (now - timedelta(minutes=5)):
                    return 0.5
                elif (now - timedelta(minutes=5)) < attempt_time:
                    return 0
                else:
                    return 1

        return 1

    def simple_token_decider(self):
        if has_learner_seen_activity(self.learner, self.activity):
            return 0
        else:
            return 1

