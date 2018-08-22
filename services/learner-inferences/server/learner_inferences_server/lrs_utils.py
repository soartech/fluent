import datetime
import requests
from requests.auth import HTTPBasicAuth


def create_learner_inference_log_xapi(verb_id, verb_en_name, activity_id, activity_en_name,
                                                obj_extensions=None, profile_id=None):
    statement = {"version": "1.0.0"}
    statement["timestamp"] = get_current_utc_time_as_str()

    statement["actor"] = {
        "name": "Learner Inference Service",
        "objectType": "Agent",
        "account": {
            "name": "learner-inference-service",
            "homePage": "insertIPAddr/learner-inferences"
        }
    }

    statement["verb"] = {
        "id": verb_id,
        "display": {
            "en": verb_en_name
        }
    }

    statement["object"] = {
        "objectType": "Activity",
        "id": activity_id,
        "definition": {
            "name": {
                "en": activity_en_name
            }
        }
    }

    if obj_extensions:
        statement["object"]["definition"]["extensions"] = obj_extensions

    if profile_id:
        statement["context"] = {
            "contextActivities": {
                "category": [
                    {
                        "id": profile_id,
                        "definition": {
                            "type": "http://adlnet.gov/expapi/activities/profile"
                        }
                    }
                ]
            }
        }

    return statement

def post_xapi_statement(statement, lrs_url, usr, pwd):
    try:
        xapi_headers = {"content-Type": "application/json",
                        "X-Experience-API-Version": "1.0.0"}
        response = requests.post(lrs_url, auth=HTTPBasicAuth(usr, pwd), json=statement, headers=xapi_headers)
        return response
    except Exception:
        #TODO: Decide what to do if Log LRS was not available.
        pass


def get_current_utc_time_as_str():
    dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return dt.isoformat()

