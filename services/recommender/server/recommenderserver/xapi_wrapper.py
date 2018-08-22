from typing import List, Union
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timezone


class XApiStatement(object):
    def __init__(self, actor_name: str, account_name: str, agent_url_id: str, verb_name: str, object: dict, context_extensions: dict=None):
        self.actor_name = actor_name
        self.account_name = account_name
        self.url_id = agent_url_id
        self.verb_name = verb_name
        self.object = object
        self.context_extensions = context_extensions
        self.display_dict = {
            "recommended": {
                "id": "https://w3id.org/xapi/dod-isd/verbs/recommended",
                "display": {
                    "en": "recommended"
                }
            },
            "logged-in": {
                "id": "http://adlnet.gov/expapi/verbs/logged-in",
                "display": {"en": "logged-in"}
            },
            "logged-out": {
                "id": "http://adlnet.gov/expapi/verbs/logged-out",
                "display": {"en": "logged-out"}
            },
            "chose": {
                "id": "https://w3id.org/xapi/dod-isd/verbs/chose",
                "display": {"en": "chose"}
            },
            "answered": {
                "id": "http://adlnet.gov/expapi/verbs/answered",
                "display": {"en-US": "answered",
                            "es-ES": "contestó"}
            },
            "asked": {
                "id": "http://adlnet.gov/expapi/verbs/asked",
                "display": {"en-US": "asked",
                            "es-ES": "preguntó"}
            },
            "attempted": {
                "id": "http://adlnet.gov/expapi/verbs/attempted",
                "display": {"en-US": "attempted",
                            "es-ES": "intentó"}
            },
            "attended": {
                "id": "http://adlnet.gov/expapi/verbs/attended",
                "display": {"en-US": "attended",
                            "es-ES": "asistió"}
            },
            "commented": {
                "id": "http://adlnet.gov/expapi/verbs/commented",
                "display": {"en-US": "commented",
                            "es-ES": "comentó"}
            },
            "completed": {
                "id": "http://adlnet.gov/expapi/verbs/completed",
                "display": {"en-US": "completed",
                            "es-ES": "completó"}
            },
            "exited": {
                "id": "http://adlnet.gov/expapi/verbs/exited",
                "display": {"en-US": "exited",
                            "es-ES": "salió"}
            },
            "experienced": {
                "id": "http://adlnet.gov/expapi/verbs/experienced",
                "display": {"en-US": "experienced",
                            "es-ES": "experimentó"}
            },
            "failed": {
                "id": "http://adlnet.gov/expapi/verbs/failed",
                "display": {"en-US": "failed",
                            "es-ES": "fracasó"}
            },
            "imported": {
                "id": "http://adlnet.gov/expapi/verbs/imported",
                "display": {"en-US": "imported",
                            "es-ES": "importó"}
            },
            "initialized": {
                "id": "http://adlnet.gov/expapi/verbs/initialized",
                "display": {"en-US": "initialized",
                            "es-ES": "inicializó"}
            },
            "interacted": {
                "id": "http://adlnet.gov/expapi/verbs/interacted",
                "display": {"en-US": "interacted",
                            "es-ES": "interactuó"}
            },
            "launched": {
                "id": "http://adlnet.gov/expapi/verbs/launched",
                "display": {"en-US": "launched",
                            "es-ES": "lanzó"}
            },
            "mastered": {
                "id": "http://adlnet.gov/expapi/verbs/mastered",
                "display": {"en-US": "mastered",
                            "es-ES": "dominó"}
            },
            "passed": {
                "id": "http://adlnet.gov/expapi/verbs/passed",
                "display": {"en-US": "passed",
                            "es-ES": "aprobó"}
            },
            "preferred": {
                "id": "http://adlnet.gov/expapi/verbs/preferred",
                "display": {"en-US": "preferred",
                            "es-ES": "prefirió"}
            },
            "progressed": {
                "id": "http://adlnet.gov/expapi/verbs/progressed",
                "display": {"en-US": "progressed",
                            "es-ES": "progresó"}
            },
            "produced": {
                "id": "https://w3id.org/xapi/dod-isd/verbs/produced",
                "display": {
                    "en-US": "produced"
                }
            },
            "registered": {
                "id": "http://adlnet.gov/expapi/verbs/registered",
                "display": {"en-US": "registered",
                            "es-ES": "registró"}
            },
            "responded": {
                "id": "http://adlnet.gov/expapi/verbs/responded",
                "display": {"en-US": "responded",
                            "es-ES": "respondió"}
            },
            "resumed": {
                "id": "http://adlnet.gov/expapi/verbs/resumed",
                "display": {"en-US": "resumed",
                            "es-ES": "continuó"}
            },
            "scored": {
                "id": "http://adlnet.gov/expapi/verbs/scored",
                "display": {"en-US": "scored",
                            "es-ES": "anotó"}
            },
            "shared": {
                "id": "http://adlnet.gov/expapi/verbs/shared",
                "display": {"en-US": "shared",
                            "es-ES": "compartió"}
            },
            "suspended": {
                "id": "http://adlnet.gov/expapi/verbs/suspended",
                "display": {"en-US": "suspended",
                            "es-ES": "aplazó"}
            },
            "terminated": {
                "id": "http://adlnet.gov/expapi/verbs/terminated",
                "display": {"en-US": "terminated",
                            "es-ES": "terminó"}
            },
            "voided": {
                "id": "http://adlnet.gov/expapi/verbs/voided",
                "display": {"en-US": "voided",
                            "es-ES": "anuló"}
            }
        }

    @property
    def actor(self):
        return {
            "objectType": "Agent",
            "name": self.actor_name,
            "account": self.account
        }

    @property
    def account(self):
        return {
            "homePage": self.url_id,
            "name": self.account_name
        }

    @property
    def verb(self):
        return self.display_dict[self.verb_name]

    @property
    def context(self):
        return {
            'extensions': self.context_extensions
        }

    @property
    def statement(self):
        return {
            "actor": self.actor,
            "verb": self.verb,
            "object": self.object,
            "context": self.context,
            "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        }


class XAPISender(object):
    def __init__(self, base_url: str, x_experience_version: str, basic_auth_user: str, basic_auth_pwd: str):
        self.url = "{}/statements/".format(base_url)
        self.usr = basic_auth_user
        self.pwd = basic_auth_pwd
        self.headers = {
            'X-Experience-API-Version': x_experience_version
        }

    def statements_post(self, statements: Union[XApiStatement, List[XApiStatement]]):
        if isinstance(statements, list):
            response = requests.post(self.url, auth=HTTPBasicAuth(self.usr, self.pwd), json=[statement.statement for statement in statements], headers=self.headers)
        else:
            response = requests.post(self.url, auth=HTTPBasicAuth(self.usr, self.pwd), json=statements.statement, headers=self.headers)
        return response
