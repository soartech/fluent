import connexion

from learner_inferences_server.models.error import Error  # noqa: E501
from learner_inferences_server.models.learner import Learner  # noqa: E501

from learner_inferences_server.config import Config
from learner_inferences_server.service_utils import ServiceJSONEncoder


def get_learner(keycloakId):  # noqa: E501
    """Obtains Learner info.

    Obtains the information of the corresponding Learner. # noqa: E501

    :param keycloakId: The Keycloak ID of the requested Learner.
    :type keycloakId: str

    :rtype: Learner
    """
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    learnerDict = store.get_learner(keycloakId)
    return learnerDict, 200, { 'ETag': store.etag_from_learner_dict(learnerDict) }

def post_learner(learnerObj):  # noqa: E501
    """Creates one Learner in Learner Profile.

    Creates a Learner, which is given as a whole object in the payload. # noqa: E501

    :param learnerObj: Learner object to add.
    :type learnerObj: dict | bytes

    :rtype: None
    """
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    returnString = store.save_learner(learnerObj, Config.SERVICE_ENDPOINT)
    return returnString, 200, { 'ETag': store.etag_from_learner_dict(learnerObj) }

def update_learner(keycloakId, learnerObj):  # noqa: E501
    """Updates Learner info.

    Updates the information of the Learner, which is given partially (one or more of the top-level properties) in the payload. # noqa: E501

    :param keycloakId: The Keycloak ID of the requested Learner.
    :type keycloakId: str
    :param learnerObj: Learner object to update.
    :type learnerObj: dict | bytes

    :rtype: None
    """
    eTag = connexion.request.headers['If-Match']
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    try:
        store.update_learner(keycloakId, learnerObj, learnerEtag=eTag)
        return 'Learner updated successfully', 200
    except ValueError as e:
        return getattr(e, 'message', repr(e)), 400

def delete_learner(keycloakId):  # noqa: E501
    """Deletes a Learner object.

    Removes the Learner from the database. # noqa: E501

    :param keycloakId: The Keycloak ID of the Learner to be deleted.
    :type keycloakId: str

    :rtype: None
    """
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    try:
        store.delete_learner(keycloakId)
        return "Learner successfully removed"
    except ValueError:
        return "Learner with ID " + keycloakId + " does not exist"
