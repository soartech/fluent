import connexion
import six

from learner_inferences_server.models.error import Error  # noqa: E501
from learner_inferences_server.models.learner import Learner  # noqa: E501
from learner_inferences_server import util

from pymongo import MongoClient
from learner_inferences_server.config import Config

def get_learners(limit=None, offset=None):  # noqa: E501
    """Obtains a collection of Learner objects from Learner Profile.

    Returns a collection of Learner objects; all learners are returned if \&quot;limit\&quot; and \&quot;offset\&quot; were not specified. # noqa: E501

    :param limit: The maximum number of objects that will be returned.
    :type limit: int
    :param offset: Determines the first object to be returned.
    :type offset: int

    :rtype: List[Learner]
    """
    if limit is None:
        limit = 0
    if offset is None:
        offset = 0

    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    learners = store.get_learners(limit, offset)
    return learners
