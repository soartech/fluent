import time
from datetime import datetime, timezone
import math

from learner_inferences_server.amqp_listener.inference_utils import convert_timestamp_to_seconds
from learner_inferences_server.config import Config
from learner_inferences_server.log_utils import print_with_time

# TODO: Class needs to be updated to current mastery levels (novice, intermediate, expert) if used again in the future.
class WeightedAvgMasteryCalculator:
    """ This class calculates mastery estimates based on the learner history and a list of MasteryProbabilities. """

    def __init__(self, min_req_observations, prob_threshold):
        """ Initializes the mastery calculator with minimum number of probabilities before attempting calculation and
            the probability threshold that will be required for mastery to be declared as 'held'.
        """
        self.MIN_REQUIRED_OBSERVATIONS = min_req_observations
        self.MASTERY_PROB_THRESHOLD = prob_threshold

    def calc_mastery_estimate(self, mastery_probabilities, competency_id):
        """ Calculates mastery estimate for the related competency. No changes to learnerDict or inference parameters. """
        mastery_probabilities.sort(key=lambda x: x['timestamp'])
        probabilities = [
            (Config.ESTIMATOR_WEIGHTS[prob['source']] * prob['probability']) for prob in mastery_probabilities
        ]

        timestamps = [
            convert_timestamp_to_seconds(prob['timestamp']) for prob in mastery_probabilities
            if convert_timestamp_to_seconds(prob['timestamp']) is not None
        ]

        mastery_probability_time_decay = 0.0
        mastery_probability = 0.0

        if mastery_probabilities is not None and len(mastery_probabilities) > 0:
            mastery_probability = self._compute_prob_mastery(probabilities)
            current_time = float(time.time())
            # Timestamps must be in seconds since epoch.
            mastery_probability_time_decay = self._compute_prob_mastery_decay(probabilities, timestamps, current_time)

        mastery_value = self._determine_mastery_val(len(mastery_probabilities), mastery_probability, mastery_probability_time_decay)

        masteryEstimate = {
            '@context': "tla-definitions.jsonld",
            '@type': Config.AMQP_MASTERY_ESTIMATE_TYPE,
            'competencyId': competency_id,
            'mastery': mastery_value,
            'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc)
        }
        return masteryEstimate

    def _determine_mastery_val(self, observations_count, mastery_probability, mastery_probability_time_decay):
        print_with_time('INFO: Determining mastery for mastery_probability = {0} and mastery_probability_time_decay = {1}'
                        .format(str(mastery_probability), str(mastery_probability_time_decay)))
        if observations_count == 0:
            return 'unknown'
        elif observations_count < self.MIN_REQUIRED_OBSERVATIONS:
            return 'indeterminate'
        elif mastery_probability >= self.MASTERY_PROB_THRESHOLD and \
             mastery_probability_time_decay < self.MASTERY_PROB_THRESHOLD:
            return 'forgotten'
        elif mastery_probability >= self.MASTERY_PROB_THRESHOLD:
            return 'held'
        else:
            return 'not held'

    def _compute_prob_mastery(self, prob_success_list):
        """
        Computes probability of mastery by weighted sum.

        :param prob_success_list: Probability of success values per each attempt.
        :return: Probability of mastery
        """
        # Limits the number of prior attempts considered to just 2
        prob_success_list = prob_success_list[-2:]
        denom = range(1, len(prob_success_list)+1)
        total = sum(denom)
        return math.fsum([
            float(prob)*((i+1)/total) for i, prob in enumerate(prob_success_list)
        ])

    def _compute_prob_mastery_decay(self, prob_success_list, time_completed_list, current_time):
        """
        Computes probability of mastery by weighted sum and time decay.

        :param prob_success_list: Probability of success values per each attempt.
        :param time_completed_list: Time of probability calculation per each attempt.
        :param current_time: Current time in seconds
        :return: Probability of mastery w/ time decay factored in.
        """
        # Limits the number of prior attempts considered to just 2
        time_completed_list = time_completed_list[-2:]
        prob_success_list = prob_success_list [-2:]
        denom = range(1, len(prob_success_list) + 1)
        total = sum(denom)
        return math.fsum([ float(prob) * self._time_decay_coeff(time_completed_list[i], current_time) *  ((i + 1) / total) for i, prob in enumerate(prob_success_list) ])

    def _time_decay_coeff(self, time_completed, current_time):
        '''
        Computes the time decay coefficient at a given time in seconds

        :param time_completed:
        :param current_time:
        :return:
        '''
        decay_coefficient = -0.1
        time_coefficient = (current_time - time_completed) / (60*60*24)
        e_val = math.exp(decay_coefficient*time_coefficient)

        return e_val