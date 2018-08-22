from datetime import datetime, timezone

from learner_inferences_server.log_utils import print_with_time
from learner_inferences_server.config import Config

class SimpleMasteryCalculator:
    """ This class calculates mastery estimates based on the learner history and a list of MasteryProbabilities. """

    def __init__(self, mastery_thresholds):
        """ Initializes the mastery calculator with an array that contains valid mastery labels and the corresponding
            minimum probabilities required to achieve each mastery. Mastery levels in the array should be sorted from
            higher to lower mastery and thresholds should be listed in decreasing order for the calculator to
            work correctly; e.g.:

            mastery_thresholds = [{'mastery': 'expert', 'threshold': 0.8},
                                  {'mastery': 'intermediate', 'threshold': 0.4},
                                  {'mastery': 'novice', 'threshold': 0.0}]

            If the threshold of the last (lowest) mastery in the array was not zero, then the calculator will return
            'unknown' for probabilities lower than that threshold.
        """
        self.MASTERY_THRESHOLDS = sorted(mastery_thresholds, key=lambda x: x['threshold'], reverse=True)

    def calc_mastery_estimate(self, mastery_probabilities, competency_id, mastery_estimates=None):
        """ Returns an instance of MasteryEstimate, calculated based on mastery_probabilities and mastery_estimates.

            This class uses only the latest probability received by learner inference service, which should be passed as
            the last element in the mastery_probabilities array (it is fine if the array contains only that most recent
            instance of MasteryProbability, but not required).
        """
        # TODO: Remove after confirming that current mastery estimates are not needed anymore.
        # if mastery_estimates:
        #     current_mastery_estimate = next((x for x in mastery_estimates if x['competencyId'] == competency_id), None)
        # else:
        #     current_mastery_estimate = None

        # Calculate mastery based on most recent mastery probability.
        latest_mastery_prob = mastery_probabilities[-1:][0]
        weighted_prob = Config.ESTIMATOR_WEIGHTS[latest_mastery_prob['source']] * latest_mastery_prob['probability']
        mastery_value, mastery_idx = self._determine_mastery_val(weighted_prob)

        masteryEstimate = {
            '@context': "tla-definitions.jsonld",
            '@type': Config.AMQP_MASTERY_ESTIMATE_TYPE,
            'competencyId': competency_id,
            'mastery': mastery_value,
            'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc)
        }
        return masteryEstimate

    def _determine_mastery_val(self, mastery_probability):
        """ Returns the first mastery level in MASTERY_THRESHOLDS array such that mastery_probability is greater or
            equal than the corresponding threshold. Returns 'unknown' if no element in the array satisfied this condition.
            Additionally, this method returns the position in the array that satisfied the threshold, or -1 if 'unknown'
            was returned.
        """
        # print_with_time('INFO: Determining mastery for mastery_probability = {0}'
        #                 .format(str(mastery_probability)))
        for index, mastery_threshold in enumerate(self.MASTERY_THRESHOLDS):
            if mastery_probability >= mastery_threshold['threshold']:
                return mastery_threshold['mastery'], index

        # At this point no mastery level satisfied threshold, return 'unknown'
        return 'unknown', -1
