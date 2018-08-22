from copy import deepcopy
import sys, os
import dateutil.parser as dateparser
import requests
import pickle
import datetime
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from learner_inferences_server.config import Config
from learner_inferences_server.amqp_listener.activity_attempts_calculator import ActivityAttemptsCalculator
from learner_inferences_server.log_utils import print_with_time, log_to_lrs
from learner_inferences_server.amqp_listener.mastery_calculators.simple_mastery_calculator import SimpleMasteryCalculator
from learner_inferences_server.lrs_utils import create_learner_inference_log_xapi


# Currently, ActivityAttemptsCalculator object gets saved after each statement is processed.
dir_path = os.path.dirname(os.path.realpath(__file__))
ACTIVITY_ATTEMPTS_CALCULATOR_FILE = "{0}/activity_attempt_calculator.pkl".format(dir_path)
if os.path.isfile(ACTIVITY_ATTEMPTS_CALCULATOR_FILE):
    ACTIVITY_ATTEMPTS_CALCULATOR = pickle.load(open(ACTIVITY_ATTEMPTS_CALCULATOR_FILE, "rb"))
else:
    ACTIVITY_ATTEMPTS_CALCULATOR = ActivityAttemptsCalculator(Config.ACTIVITY_TIMEOUT_SECS)


# TODO: Use only camelCase or snake_case

def process_raw_inference(raw_inference):
    """ Currently processes messages of type MasteryProbability and Context. """
    if '@context' not in raw_inference or raw_inference['@context'] == None:
        raw_inference['@context'] = 'tla-declarations.jsonld'

    if raw_inference['@type'] == Config.AMQP_MASTERY_PROB_TYPE:
        return process_mastery_prob(raw_inference)
    elif raw_inference['@type'] == Config.AMQP_CONTEXT_TYPE:
        return process_context(raw_inference)
    elif raw_inference['@type'] == Config.AMQP_ASSERTION_TYPE:
        return process_cass_assertion(raw_inference)
    else:
        #TODO: Decide what to do in this case.
        return {}

def process_experience(statement):
    """  """
    terminated_activities = ACTIVITY_ATTEMPTS_CALCULATOR.assess_activities(statement)
    if terminated_activities and len(terminated_activities) > 0:
        _increase_activity_attempt_counters(terminated_activities)

    pickle.dump(ACTIVITY_ATTEMPTS_CALCULATOR, open(ACTIVITY_ATTEMPTS_CALCULATOR_FILE, "wb"))

def process_mastery_prob(mastery_prob):
    """ Process a new instance of MasteryProbability that is passed as parameter.

        This function loads user data from store, updates mastery information and save the learner back into store.
        If the new information triggered a change in mastery estimates, then this function outputs a dictionary
        that corresponds to type LearnerInference, which learner inference service will communicate in real time.
    """
    # Get learner from store
    # TODO: For performance, load only necessary fields.

    if not _useful_mastery_prob(mastery_prob):
        return {}

    mastery_prob['competencyId'] = sanitize_competency_id(mastery_prob['competencyId'])

    learner_id = get_id_from_learnerId(mastery_prob['learnerId'])
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)

    learner_dict, _ = store.lock_learner(learner_id)

    # NOTE: this will be the case if we fail to lock the learner within the time limit
    if learner_dict is None:
        return {}

    try:
        if mastery_prob['source'] == Config.MASTERY_ESTIMATOR_COMPETENCY_COUNTS:
            _increase_competency_attempt_counter(learner_dict, mastery_prob)

        if mastery_prob['source'] in Config.VALID_ESTIMATORS:
            if 'masteryProbabilities' not in learner_dict or learner_dict['masteryProbabilities'] == None:
                learner_dict['masteryProbabilities'] = []

            # TODO: Apparently only reason for not doing learner_dict['masteryProbabilities'].append(mastery_prob) is diff in
            #       the name of one field. That could be corrected later, for not having two separate data models just because
            #       of this diff.
            latest_mastery_prob = {
                '@context': mastery_prob.get('@context', None),
                '@type': mastery_prob['@type'],
                'competencyId': mastery_prob['competencyId'],
                'probability': mastery_prob['masteryProbability'],
                'timestamp': mastery_prob['timestamp'],
                'source': mastery_prob['source']
            }
            learner_dict['masteryProbabilities'].append(latest_mastery_prob)

            newEstimate, learner_dict = _get_mastery_estimate(learner_dict, latest_mastery_prob)

            # Save updates for mastery probabilities and competency counter.
            learner_dict = recursivelyConvertTimestampsInDict(learner_dict)
            store.update_learner(learner_id, learner_dict, lockedLearner=True)

            learnerInference = {
                '@context': mastery_prob.get('@context', None),
                '@type': Config.AMQP_LEARNER_INFERENCE_TYPE,
                'timestamp': mastery_prob['timestamp'],
                'learnerId': learner_id,
                'masteryEstimates': newEstimate
            }

            return learnerInference
    except Exception as e:
        print_with_time("ERROR: Exception while processing mastery probability {0}: {1}"
                        .format(str(mastery_prob)), str(e))
        raise e
    finally:
        store.unlock_learner(learner_id)

    # No processing occurred.
    return {}

def process_context(context):
    # Context Detector not implemented for August's study.
    pass

def _useful_mastery_prob(mastery_prob):
    useful_prob = 'learnerId' in mastery_prob and 'competencyId' in mastery_prob and \
                  (mastery_prob['source'] in Config.VALID_ESTIMATORS or
                   mastery_prob['source'] == Config.MASTERY_ESTIMATOR_COMPETENCY_COUNTS)
    return useful_prob

def _increase_competency_attempt_counter(learner_dict, mastery_prob):
    """This function updates counter but does not store changes, as learner is stored by the function calling this one."""
    if 'competencyAttemptCounters' in learner_dict:
        competency_counters = learner_dict['competencyAttemptCounters']
    else:
        competency_counters = []
        learner_dict['competencyAttemptCounters'] = competency_counters

    competency_id = mastery_prob['competencyId']
    competency_counter = next((x for x in competency_counters if x['competencyId'] == competency_id), None)

    if competency_counter:
        updated_counter = competency_counter['attempts'] + 1
        competency_counter['attempts'] = updated_counter
        competency_counter['lastAttemptDateTime'] = mastery_prob['timestamp']
    else:
        updated_counter = 1
        competency_counter = {
            "@context": "tla-declarations.jsonld",
            "@type": "CompetencyAttemptCounter",
            "competencyId": competency_id,
            "attempts": updated_counter,
            "lastAttemptDateTime": mastery_prob['timestamp']
        }

        competency_counters.append(competency_counter)

    print_with_time('INFO: Updated competency attempt counter to {0} for learner {1}, competency {2}'
                    .format(str(updated_counter), learner_dict['identifier'], competency_id))
    log_data = {
        "learnerId": learner_dict['identifier'],
        "competencyId": competency_id,
        "attemptCounter": competency_counter['attempts']
    }
    statement = create_learner_inference_log_xapi(verb_id="https://w3id.org/xapi/dod-isd/verbs/saved", verb_en_name="saved",
                                                  activity_id="insertIPAddr/save-competency-attempt-counter",
                                                  activity_en_name="Save Competency Attempt Counter",
                                                  obj_extensions={"insertIPAddr/learner-inferences/log-data": log_data},
                                                  profile_id="https://w3id.org/xapi/dod-isd/v1.0")
    if Config.LOG_TO_LRS:
        log_to_lrs(statement)
    if Config.LOG_XAPI_TO_FILE:
        print_with_time("[XAPI LOG]: {}".format(json.dumps(statement)))

def process_cass_assertion(raw_inference):
    """ Maps an Assertion message to MasteryProbability message, and process accordingly. """
    assertion = _retrieve_assertion_from_CASS(raw_inference)
    mastery_prob = _map_assertion_to_mastery_prob(assertion)
    return process_mastery_prob(mastery_prob)

def _retrieve_assertion_from_CASS(raw_inference):
    """This method relies in cass-worker service to retrieve the corresponding Assertion.

        An example query that can be used for testing purposes, on the same computer where cass-worker is running:
        curl http://localhost:9722/decrypt?url=insertCassBase/api/data/insertCassSchemaUrl.0.3.Assertion/7e4a0aa8-1504-4253-9c54-01b508ddf529/1508282829855

        This request would generate a response as in the following example:

        {
        "@context": "http://insertCassSchemaUrl/0.3",
        "@id": "insertCassBase/api/data/insertCassSchemaUrl.0.3.Assertion/7e4a0aa8-1504-4253-9c54-01b508ddf529/1508282829855",
        "@owner": [
            "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl5Zsr3KlThU+OGbkT+Ld24j0u2AUMnh7YU7+/PiKzJaR/zv06RFALl+m2kmNXFgnsIZQeE4OvHWXptJsghIlrL36NbQwrpknXglqQ9dPHIKrdlvnSvvPvWSBcs+O2eKJg4A2wSjx5Ls6lJRijRLlIwRC/SD8tx/UeaakQ5b/kyyaDsL3ScyT5yUzICBR0xIp+0HRLVkxG9t2BW1/Gnw78SYUZKZT2a0c01d5rzvXDH9VFfYDANG6oep/AmDOhVLI3qG8MYVKnyVKK2/3VIl+EOIYPxbGasJWp7vredxtCEQfbzQI8D9DfbizYxSRuxmcU++mLhGWdyD7YgrOSQvFkwIDAQAB-----END PUBLIC KEY-----"
        ],
        "@signature": [
            "HEkea0ev7SKBHJ4ZrO1iMrGHMyLNfZRt79S5LdUQn20tmYynrLgU+xJgbTWHI5L/K28xuSSB5aBkOv5PYjc4TWAntseOWh9K+G7KGCors49gWTuehl6Sj1gxSTy28Ha9u3Ah/nKMweCAFMWEuNLMM+DhCuS3DVSY3sMef58Mijehl51UFmtIGEfMPMRmAcM7TRfapYOGig3NdheWVBJbeOAz+/ufG7usIMDgVUfpGNVUQsRFtk+33I04zJ4Klsz98VXSVoX4+GJAvsWV8FfRLXOihBerrLMZBRlL9TFtG4lP39x6ZqwgI1AcLDr57FnQKszS7Dtob6KVA8CxWX3ucA=="
        ],
        "@type": "Assertion",
        "agent": "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl5Zsr3KlThU+OGbkT+Ld24j0u2AUMnh7YU7+/PiKzJaR/zv06RFALl+m2kmNXFgnsIZQeE4OvHWXptJsghIlrL36NbQwrpknXglqQ9dPHIKrdlvnSvvPvWSBcs+O2eKJg4A2wSjx5Ls6lJRijRLlIwRC/SD8tx/UeaakQ5b/kyyaDsL3ScyT5yUzICBR0xIp+0HRLVkxG9t2BW1/Gnw78SYUZKZT2a0c01d5rzvXDH9VFfYDANG6oep/AmDOhVLI3qG8MYVKnyVKK2/3VIl+EOIYPxbGasJWp7vredxtCEQfbzQI8D9DfbizYxSRuxmcU++mLhGWdyD7YgrOSQvFkwIDAQAB-----END PUBLIC KEY-----",
        "assertionDate": 1508308007000,
        "competency": "insertCassBase/api/custom/data/insertCassSchemaUrl.0.2.Competency/49667dd5-a700-4f6c-b5ad-97d4a2cafe13",
        "confidence": "0.95",
        "decayFunction": "linear",
        "expirationDate": 1539844007000,
        "subject": "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl5Zsr3KlThU+OGbkT+Ld24j0u2AUMnh7YU7+/PiKzJaR/zv06RFALl+m2kmNXFgnsIZQeE4OvHWXptJsghIlrL36NbQwrpknXglqQ9dPHIKrdlvnSvvPvWSBcs+O2eKJg4A2wSjx5Ls6lJRijRLlIwRC/SD8tx/UeaakQ5b/kyyaDsL3ScyT5yUzICBR0xIp+0HRLVkxG9t2BW1/Gnw78SYUZKZT2a0c01d5rzvXDH9VFfYDANG6oep/AmDOhVLI3qG8MYVKnyVKK2/3VIl+EOIYPxbGasJWp7vredxtCEQfbzQI8D9DfbizYxSRuxmcU++mLhGWdyD7YgrOSQvFkwIDAQAB-----END PUBLIC KEY-----",
        "learnerId": "133e4576-e89b-21d4-a456-42465543a0b1"
        }

        Note: CASS' Assertion class does not contain property "learnerId". This property is added by the CASS Worker
        service that is called here.
    """
    template_url = 'http://{worker_host}:{worker_port}/decrypt?url={assertion_url}'
    url =  template_url.format(
        worker_host = Config.CASS_WORKER_HOST,
        worker_port = str(Config.CASS_WORKER_PORT),
        assertion_url = raw_inference['accessUrl']
    )

    # TODO: Microservice cass-worker currently can return an Assertion with learnerId = "error" (e.g., LRS not available).
    # We need to discuss approach to take in that case and whether changes are needed from CASS.

    try:
        response = requests.get(url, timeout=0.5).json()
        return response
    except:
        pass
        #TODO: What's the most appropriate behavior if cass-worker was unavailable?

def _map_assertion_to_mastery_prob(assertion):
    learner_id = get_id_from_learnerId(assertion['subject'])

    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    try:
        attempt_counters = store.get_learner_property(learner_id, 'competencyAttemptCounters')
    except ValueError as e:
        #TODO: What to do if learner is not in DB? That shouldn't happen, but it happens now after reprovisioning ST VM.
        attempt_counters = None
        pass

    if attempt_counters is not None:
        attempt_counter = next((x for x in attempt_counters if x['competencyId'] == assertion['competency']), None)
        next_attempt = (attempt_counter['attempts'] + 1) if attempt_counter else 1
    else:
        next_attempt = 1

    mastery_prob = {
        '@context': 'tla-declarations.jsonld',
        '@type': 'MasteryProbability',
        'learnerId': assertion['subject'],
        'timestamp': assertion['assertionDate'],
        'competencyId': assertion['competency'],
        'nextAttempt': next_attempt,
        'masteryProbability': _get_mastery_prob_from_assertion(assertion),
        'confidence': assertion['confidence'],
        'source': 'CASS'
    }

    return mastery_prob

def _get_mastery_prob_from_assertion(assertion):
    """ The Mapping is as follows:
        If Assertion's optional property "negative" was present and set to True, then field "confidence" maps to
        a mastery probability, linearly, as follows: [0, 1] => [0.5, 0]. Otherwise, Assertion's field "confidence"
        maps to a mastery probability, linearly, as follows: [0, 1] => [0.5, +1].
    """
    # Assumption: Field "confidence" will always be part of an Assertion object.
    confidence = assertion['confidence']
    if 'negative' in assertion and assertion['negative']:
        new_bottom = 0.5
        new_top = 0
    else:
        new_bottom = 0.5
        new_top = 1

    mastery_prob = confidence * (new_top - new_bottom) + new_bottom

    # Check boundaries just in case result was not exact.
    if mastery_prob < 0:
        mastery_prob = 0
    elif mastery_prob > 1:
        mastery_prob = 1

    return mastery_prob

def _increase_activity_attempt_counters(terminated_activities):
    """The input is a dictionary that contains fields 'learnerId','activityId', 'timestamp'."""
    store = Config.STORE_CLIENT(Config.STORE_HOST, Config.STORE_PORT, Config.STORE_DB)
    for activity_attempt in terminated_activities:
        learner_id = activity_attempt['learnerId']
        activity_id = activity_attempt['activityId']

        try:
            attempt_counters = store.get_learner_property(learner_id, 'activityAttemptCounters') #Might return None.
            for i, attempt in enumerate(attempt_counters):
                if type(attempt['lastAttemptDateTime']) == datetime.datetime:
                    attempt_counters[i]['lastAttemptDateTime'] = attempt['lastAttemptDateTime'].replace(tzinfo=datetime.timezone.utc).isoformat()
        except ValueError as e:
            # Apparently learner is not in DB. That shouldn't happen, so we are logging this as error and
            # move on to the next update.
            print_with_time('ERROR: Attempted to update activityAttemptCounters for learner with Id {0} but impossible to retrieve learner data from DB.'
                            .format(learner_id))
            continue

        if attempt_counters is not None:
            attempt_counter = next((x for x in attempt_counters if x['activityId'] == activity_id), None)
        else:
            attempt_counters = []
            attempt_counter = None

        if attempt_counter:
            attempt_counter['attempts'] = attempt_counter['attempts'] + 1
            attempt_counter['lastAttemptDateTime'] = activity_attempt['terminatedTimestamp']
        else:
            attempt_counter = {
                "@context": "tla-declarations.jsonld",
                "@type": "ActivityAttemptCounter",
                "activityId": activity_id,
                "attempts": 1,
                "lastAttemptDateTime": activity_attempt['terminatedTimestamp']
            }

            attempt_counters.append(attempt_counter)
        dikt = {'activityAttemptCounters': attempt_counters}
        dikt = recursivelyConvertTimestampsInDict(dikt)
        store.update_learner(learner_id, dikt, learnerEtag=False)

        print_with_time('INFO: Set activity attempt counter to {0} for user {1}, activity {2}'
                        .format(str(attempt_counter['attempts']), learner_id, activity_id))
        log_data = {
            "learnerId": learner_id,
            "activityId": activity_id,
            "attemptCounter": attempt_counter['attempts']
        }
        statement = create_learner_inference_log_xapi(verb_id="https://w3id.org/xapi/dod-isd/verbs/saved", verb_en_name="saved",
                                                      activity_id="insertIPAddr/save-activity-attempt-counter",
                                                      activity_en_name="Save Activity Attempt Counter",
                                                      obj_extensions={"insertIPAddr/learner-inferences/log-data": log_data},
                                                      profile_id="https://w3id.org/xapi/dod-isd/v1.0")
        if Config.LOG_TO_LRS:
            log_to_lrs(statement)
        if Config.LOG_XAPI_TO_FILE:
            print_with_time("[XAPI LOG]: {}".format(json.dumps(statement)))

def get_id_from_learnerId(learnerId):
    """ Returns the portion of the learnerId that corresponds to ID field in database. """
    return learnerId.split('/')[-1]

def _get_mastery_estimate(learnerDict, latest_mastery_prob):
    """ Calculates mastery estimates based on inference and returns new mastery estimate and updated learnerDict. """
    competency_id = latest_mastery_prob.get('competencyId', None)

    if 'masteryEstimates' not in learnerDict or learnerDict['masteryEstimates'] == None:
        learnerDict['masteryEstimates'] = []

    # TODO: Here newEstimate.timestamp is a string, while timestamps loaded in masteryEstimate collection are datetimes.
    #       This is not causing any issue, as method to update learner in DB processes its input and one of the actions
    #       is to convert datetimes that were strings to datetimes. Still, we might want to get all types in sync here.
    mastery_calculator = SimpleMasteryCalculator(Config.MASTERY_THRESHOLDS)
    newEstimate = mastery_calculator.calc_mastery_estimate([latest_mastery_prob], competency_id)

    estimateToUpdate = None
    for estimate in learnerDict['masteryEstimates']:
        if newEstimate['competencyId'] == estimate['competencyId']:
            estimateToUpdate = estimate
            break

    if estimateToUpdate is not None:
        if 'pastMasteryEstimates' not in learnerDict or learnerDict['pastMasteryEstimates'] == None:
            learnerDict['pastMasteryEstimates'] = []
        learnerDict['pastMasteryEstimates'].append(estimateToUpdate)
        learnerDict['masteryEstimates'].remove(estimateToUpdate)

    # Always add the new estimate.
    learnerDict['masteryEstimates'].append(newEstimate)

    return newEstimate, learnerDict

def convert_timestamp_to_seconds(timestp):
    if isinstance(timestp, str):
        return float(dateparser.parse(timestp).timestamp())
    elif isinstance(timestp, datetime.datetime):
        return float(timestp.timestamp())
    else:
        return None

def recursivelyConvertTimestampsInDict(d: dict) -> dict:
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = recursivelyConvertTimestampsInList(value)
        elif isinstance(value, dict):
            d[key] = recursivelyConvertTimestampsInDict(value)
        elif isinstance(value, datetime.datetime):
            d[key] = convertDatetime(value)
    return d

def recursivelyConvertTimestampsInList(lst: list) -> list:
    for i in range(len(lst)):
        if isinstance(lst[i], list):
            lst[i] = recursivelyConvertTimestampsInList(lst[i])
        elif isinstance(lst[i], dict):
            lst[i] = recursivelyConvertTimestampsInDict(lst[i])
        elif isinstance(lst[i], datetime.datetime):
            lst[i] = convertDatetime(lst[i])
    return lst

def convertDatetime(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat()

def sanitize_competency_id(competency_id: str):
    """ This method is used to sanitize potentially invalid competency Ids coming from CASS and other clients that could
        be fixed, based on the format agreed for the 2018 study. Two fixes are considered, described by the following examples:

        Case 1. Replace 'http' by 'https' in a competency URL:

        Case 2. Remove CASS version number from the end of a competency URL:
            "https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037/1526575157983"

            will become:

            "https://insertCassUrl/api/data/insertCassSchemaUrl.0.3.Competency/c8fadde7-c51e-4cfe-9d52-4e88aaad7037"

        Other wrong competency Ids will trigger a ValueError exception.
    """
    competency_id = competency_id.replace("http://", "https://", 1)

    pieces = competency_id.split('/')
    last_term = pieces[-1:][0]

    try:
        val = int(last_term)
        # If not exception triggered then assume version number was added to competency Id.
        print_with_time("WARN: Competency Id ({0}) seems to have version number at the end, cutting it accordingly.".format(competency_id))
        competency_id = '/'.join(pieces[0:-1])
    except Exception:
        pass # No problem, as last term SHOULD NOT be an int.

    return competency_id

