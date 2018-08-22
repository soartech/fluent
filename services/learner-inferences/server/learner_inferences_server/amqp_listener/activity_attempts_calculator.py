from datetime import datetime
import dateutil.parser

from learner_inferences_server.config import Config


class ActivityAttemptsCalculator:
    """ This class estimates activity attempts based on a stream of xAPI statements.

    xAPI statements are received one at a time.  Monitoring learners' use of activities allows
    estimating activity attempts. Basically, this class decides whether the counter for a learner's
    activity attempts should be increased, based on two rules:

    (1) A terminated statement was received.
    (2) No statements has come from an non-terminated activity within a time window defined by activity_timeout (in secs).

    activity_timeout: Time in secs after which an activity's session should be declared terminated.
    """

    def __init__(self, activity_timeout):
        """ Initializes with a certain time_window specified in seconds."""
        self._activity_timeout = activity_timeout
        self._activity_trackers = {}

    def assess_activities(self, statement):
        """ Assess statement linked to learner and activity. Returns list of activity attempt notifications or [].

            To avoid setting up timers to check for potential timeouts and the corresponding multi-threading implications,
            a first implementation uses an approximate approach: All tracked active sessions are checked
            against activity_timeout whenever a statement is processed. Activities that are deemed terminated by this
            process are included in the output list.
        """
        terminated_activities = []

        try:
            activity_id = self._get_activity_id_from_xapi(statement)
            learner_id = statement["actor"]["account"]["name"]

            # Attempt to retrieve name for debugging/logging purposes, but it's not a mandatory field in xAPI.
            try:
                learner_name = statement["actor"]["name"]
            except:
                learner_name = None

            timestamp = statement['timestamp']
            unix_time = self._get_unix_time_from_iso_8601(timestamp)

            # Before anything else, stop tracking activities that are stale w.r.t. timestamp of new statement.
            if self._activity_timeout > 0:
                terminated_activities = self._get_timed_out_activities(unix_time)
                for actv in terminated_activities:
                    self._remove_from_activity_trackers(actv['activityId'], actv['learnerId'])

                # Add new statement to tracker even if verb was 'terminated',
                # just in case we missed prior statements from activity.
                self._add_to_activity_trackers(activity_id, learner_id, learner_name, timestamp)

            # Process activity as terminated if verb was terminated or completed (they are mutually exclusive).
            verb = statement['verb']['id']
            if verb == Config.TERMINATED_VERB_ID or verb == Config.COMPLETED_VERB_ID:
                terminated_activities.append({
                    'activityId': activity_id,
                    'learnerId': learner_id,
                    'learnerName': statement["actor"]["name"],
                    'terminatedTimestamp': timestamp
                })
            
                if self._activity_timeout > 0:    
                    self._remove_from_activity_trackers(activity_id, learner_id)
        except:
            # Assuming statement does not contain all required information, so no problem.
            pass

        return terminated_activities

    def _get_activity_id_from_xapi(self, statement):
        """ Determines the right property to read the activity id from.

            If statement['object']['id'] contains a dash (i.e., it denotes a question inside an activity) then
            ActivityAttemptsCalculator will rely on statement['context']['contextActivity']['parent'][0]['id]
            to obtain the value of activityId.

        """
        activity_id = statement['object']['id']

        if '-' in activity_id:
            try:
                activity_id = statement['context']['contextActivity']['parent'][0]['id']
            except:
                # Fall back to use text to the left of dash if parent Id could not been retrieved.
                activity_id = statement['object']['id'].split('-')[0]

        return activity_id

    def _add_to_activity_trackers(self, activity_id, learner_id, learner_name, timestamp):
        if activity_id not in self._activity_trackers:
            self._activity_trackers[activity_id] = {}
        if learner_id not in self._activity_trackers[activity_id]:
            self._activity_trackers[activity_id][learner_id] = {}

        unix_timestamp = self._get_unix_time_from_iso_8601(timestamp)
        self._activity_trackers[activity_id][learner_id]['last_seen_unix_time'] = unix_timestamp
        self._activity_trackers[activity_id][learner_id]['learnerName'] = learner_name

    def _remove_from_activity_trackers(self, activity_id, learner_id):
        try:
            del self._activity_trackers[activity_id][learner_id]
        except:
            # Apparently item was not there already.
            pass

    def _get_timed_out_activities(self, ref_unix_time):
        """ Return information about activities that have timed out, based on ref_unix_time."""
        timed_out_activities = []
        for activity_id, activity_data in self._activity_trackers.items():
            for learner_id, learner_data in activity_data.items():
                if (ref_unix_time - learner_data['last_seen_unix_time']) > self._activity_timeout:
                    termination_time = learner_data['last_seen_unix_time'] + self._activity_timeout
                    timed_out_activities.append({
                        'activityId': activity_id,
                        'learnerId': learner_id,
                        'learnerName': learner_data['learnerName'],
                        'terminatedTimestamp': self._get_iso_8601_from_unix_time(termination_time)
                    })

        return timed_out_activities

    def _get_unix_time_from_iso_8601(self, iso_datetime):
        # TODO: (1) Is this fine or do we need something like:
        #       unix_timestamp = a_datetime.replace(tzinfo=timezone.utc).timestamp()
        unix_timestamp = dateutil.parser.parse(iso_datetime).timestamp()
        return unix_timestamp

    def _get_iso_8601_from_unix_time(self, unix_time):
        iso_datetime = datetime.fromtimestamp(unix_time).isoformat()
        return iso_datetime

