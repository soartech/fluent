import requests
from typing import List
import csv, json


def get_existing_learners():
    learner_list = requests.get("insertIPAddr/learner-inferences/learners").json()
    return learner_list

def read_users_from_csv():
    user_list = []
    with open('keycloak-users.csv') as csvfile:
        keycloak_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        headers = next(keycloak_reader)
        print(headers)
        for row in keycloak_reader:
            user = {}
            for idx, key in enumerate(headers):
                user[key] = row[idx]
            user_list.append(user)
    print(user_list)
    return user_list


def load_learners_into_server():
    learner_list = read_users_from_csv()
    learner_list = read_users_from_csv()
    existing_learners = get_existing_learners()
    existing_learner_IDs = [learner["identifier"] for learner in existing_learners]
    existing_learner_emails = [learner.get("email", "") for learner in existing_learners]

    for incoming_learner_dict in learner_list:
        learner_id = incoming_learner_dict.get("ID", "")
        learner_email = incoming_learner_dict.get("EMAIL", "")

        use_patch = False
        if learner_id in existing_learner_IDs: # or learner_email in existing_learner_emails:
            #print("User with email " + (learner_email or "[BLANK]") + " already exists. using Patch.")
            use_patch = True

        learner_first_name = incoming_learner_dict.get("FIRST_NAME", "")
        learner_last_name = incoming_learner_dict.get("LAST_NAME", "")
        if learner_last_name:
            learner_name = learner_first_name + " " + learner_last_name
        else:
            learner_name = learner_first_name

        if not (learner_id or learner_name or learner_email):
            continue

        #print(json.dumps(cleared_learner_dict))

        response = ""
        if use_patch:
            cleared_learner_dict = {
                "name": learner_name,
                "email": learner_email
            }
            print("PATCHing user: " + cleared_learner_dict["name"])
            get_response = requests.get("insertIPAddr/learner-inferences/learners/"+learner_id)
            etag = get_response.headers["ETag"]
            response = requests.patch("insertIPAddr/learner-inferences/learners/"+learner_id, json=cleared_learner_dict, headers={"If-Match": etag})
        else:
            # Create a new dict object
            cleared_learner_dict = {
                "@context": "tla-declarations.jsonld",
                "@type": "Learner",
                "identifier": learner_id,
                "name": learner_name,
                "email": learner_email,
                "activityAttemptCounters": [],
                "bored": False,
                "competencyAchievements": [],
                "competencyAttemptCounters": [],
                "confused": False,
                "currentActivities": [],
                "currentDeviceCategories": [],
                "currentPlatforms": [],
                "eureka": False,
                "flow": False,
                "frustrated": False,
                "goals": [],
                "lastActivityHard": False,
                "lastActivityUseful": False,
                "mainEntityOfPage": "string",
                "masteryEstimates": [],
                "masteryProbabilities": [],
                "pastGoals": [],
                "pastMasteryEstimates": [],
                "sleepy": False
            }
            print("POSTing user: " + cleared_learner_dict["name"])
            response = requests.post("insertIPAddr/learner-inferences/learners", json=cleared_learner_dict)
        print(response)
        print(response.json())

load_learners_into_server()
