from hashlib import md5
import time

from bson import json_util
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from learner_inferences_server.models.learner import Learner
from learner_inferences_server.service_utils import ServiceJSONEncoder
from learner_inferences_server.decorators import retry_decorator

# Retry on AutoReconnect errors, maximum was not specified in Config because of circular dependency (to address later)
STORE_MAX_RETRIES = 3
LOCK_MAX_WAIT_MS = 20000
retry_auto_reconnect = retry_decorator(STORE_MAX_RETRIES, (ConnectionFailure,))

class MongoLearnerStoreClient(object):
    """This class can be used to access data in a MongoDB database."""

    def __init__(self, mongo_host, mongo_port, mongo_db, etag_hash=md5):
        self._mongo_host = mongo_host
        self._mongo_port = mongo_port
        self._mongo_db = mongo_db
        self._etag_hash = etag_hash

    @retry_auto_reconnect
    def get_learners(self, limit, offset):
        """Returns a list of learners, restricted in length by parameters limit and offset."""
        learnerDictList = []
        db = self._get_mongo_db()
        for learnerDict in db.learners.find({}, {'_id': 0}).limit(limit).skip(offset):
            learnerDictList.append(learnerDict)
        return learnerDictList

    @retry_auto_reconnect
    def get_learners_with_properties(self, properties):  # noqa: E501
        """ Returns the values of various properties of a learner, given the learner's _id value and list of
            properties.
        """
        db = self._get_mongo_db()
        filters = {'_id': 0}
        for prop in properties:
            filters[prop] = 1

        learnerDictList = []
        for learnerDict in db.learners.find({}, filters):
            # Make sure absent properties are included as None.
            for prop in properties:
                if prop not in learnerDict:
                    learnerDict[prop] = None

            learnerDictList.append(learnerDict)

        return learnerDictList

    @retry_auto_reconnect
    def get_learner(self, learnerId):  # noqa: E501
        """Obtains Learner info given the value of the _id property, which is passed as a string."""
        db = self._get_mongo_db()
        learnerDict = db.learners.find_one({'identifier': learnerId}, {'_id': 0})
        return learnerDict

    @retry_auto_reconnect
    def get_learner_property(self, learnerId, property):  # noqa: E501
        """Returns the value of a single property of a learner, given the learner's _id value."""
        db = self._get_mongo_db()
        learnerDict = db.learners.find_one({'identifier': learnerId}, {'_id': 0, property: 1})
        if learnerDict is None:
            raise ValueError('No learner with identifier {0} in DB.'.format(learnerId))
        return learnerDict[property] if property in learnerDict else None

    @retry_auto_reconnect
    def get_learner_properties(self, learnerId, properties):  # noqa: E501
        """ Returns the values of various properties of a learner, given the learner's _id value and list of
            properties.
        """
        db = self._get_mongo_db()
        filters = {'_id': 0}
        for prop in properties:
            filters[prop] = 1

        learnerDict = db.learners.find_one({'identifier': learnerId}, filters)
        if learnerDict is None:
            raise ValueError('No learner with identifier {0} in DB.'.format(learnerId))

        # Make sure absent properties are included as None.
        for prop in properties:
            if prop not in learnerDict:
                learnerDict[prop] = None

        return learnerDict

    @retry_auto_reconnect
    def delete_learner(self, learnerId):  # noqa: E501
        """Deletes a Learner object from the database given the value of the_id property."""
        db = self._get_mongo_db()
        dict = db.learners.find_one({'identifier': learnerId})
        if dict is not None:
            db.learners.remove({'identifier': learnerId})
        else:
            raise ValueError('Learner with ID ' + learnerId + ' does not exist')

    @retry_auto_reconnect
    def save_learner(self, learnerObj, service_endpoint=None):  # noqa: E501
        """Creates one Learner in Learner Profile, assigning an _id at the time of storing it."""
        learnerObj = Learner.from_dict(learnerObj)
        learnerDict = ServiceJSONEncoder(include_nulls=False).default(learnerObj)
    
        db = self._get_mongo_db()
        learner = db.learners.find_one({'identifier': learnerDict['identifier']}, {'_id': 0})
        if learner is None:
            db.learners.insert_one(learnerDict)
            return 'Learner with ID ' + learnerDict['identifier'] + ' successfully created'
        else:
            return 'Learner with ID ' + learnerDict['identifier'] + ' already exists'

    @retry_auto_reconnect
    def update_learner(self, learnerId, learnerObj, learnerEtag=None, lockedLearner=False):  # noqa: E501
        """Updates Learner info, which is given partially in a dictionary."""
        learnerObj = Learner.from_dict(learnerObj)
        learnerDict = ServiceJSONEncoder(include_nulls=False).default(learnerObj)

        db = self._get_mongo_db()

        if lockedLearner:
            learner, db_etag = learnerObj, None
        else:
            learner, db_etag = self.lock_learner(learnerId, db)

        if learner is not None:
            try:
                if learnerEtag != False and str(db_etag) != str(learnerEtag):
                    raise ValueError("ETag '{}' does not match current stored revision '{}', so learner has been updated in the meantime.  Please update your copy and try again.".format(learnerEtag, db_etag))
                update_id = learnerDict.get('identifier', None)
                if update_id is not None and str(update_id) != str(learnerId):
                    raise ValueError('Learner IDs do not match, request denied (Posted ID: {}, Learner ID: {}).'.format(update_id, learnerId))

                # TODO - this should probably be checked for elsewhere.
                learnerDict = account_for_emotion_update(learnerDict)

                db.learners.update({'identifier': learnerId}, {'$set': learnerDict})
            finally:
                if not lockedLearner:
                    self.unlock_learner(learnerId, db)
        else:
            # TODO: fix this to distinguish these two failure cases
            #if learner is None:
            #    raise ValueError('No learner with identifier = {0} in DB.'.format(learnerId))
            raise Exception("Failed to lock learner with ID {} within maximum number of retries.".format(learnerId))

    @retry_auto_reconnect
    def unlock_learner(self, learnerId, db=None):
        if db is None:
            db = self._get_mongo_db()

        db.learners.update_one({'identifier': learnerId}, {'$unset': {'_writelocked': '' } })

    @retry_auto_reconnect
    def lock_learner(self, learnerId, db=None):

        start_time = 1000 * time.time()
        cur_time = start_time

        if db is None:
            db = self._get_mongo_db()

        while (cur_time - start_time) < LOCK_MAX_WAIT_MS:
            learner = db.learners.find_one_and_update({'identifier': learnerId}, {'$set': {'_writelocked': True } })

            if not learner:
                return None, None
            # The returned document is the state before the above update,
            # so if the lock succeeded, then it did not have had the _writelocked
            # field present pre-change, but now it does post-change
            elif '_writelocked' not in learner:
                del learner['_id']
                return learner, self.etag_from_learner_dict(learner)
            else:
                time.sleep(0)
                cur_time = 1000 * time.time()

        return None, None

    @retry_auto_reconnect
    def _get_mongo_db(self):
        client = MongoClient(self._mongo_host, self._mongo_port)
        db = client[self._mongo_db]
        return db

    def etag_from_learner_dict(self, learnerDict):
        """
            Expects the learner document taken directly from Mongo, with only the _id field removed.  It is important
            that all fields be present so we can distinguish if _anything_ has changed when updates are received!
        """
        # TODO: If there's a better way to reliably hash data from MongoDB, please use it to replace the code below
        json_string = json_util.dumps(learnerDict, json_options=json_util.CANONICAL_JSON_OPTIONS, sort_keys=True)
        md5sum = self._etag_hash()
        md5sum.update(json_string.encode('UTF-8'))
        return md5sum.hexdigest()


def account_for_emotion_update(learnerDict) -> dict:
    emotions = {
        "bored",
        "confused",
        "frustrated",
        "flow",
        "eureka"
    }

    if len(emotions.intersection(set(learnerDict.keys()))) > 0:
        for emotion in emotions:
            if emotion not in learnerDict:
                learnerDict[emotion] = False

    return learnerDict

if __name__ == '__main__':
    # Values to be maintained manually by developer, according to it's own test data.
    print('Testing against MongoDB on localhost')
    store = MongoLearnerStoreClient('127.0.0.1', 27017, 'tla2018')
    full_learner = store.get_learner('https://learner-profile/learners/5ae335e264e76ec4407dfbb0')
    learner_prop = store.get_learner_property('https://learner-profile/learners/5ae335e264e76ec4407dfbb0',
                                              'activityAttemptCounters')

