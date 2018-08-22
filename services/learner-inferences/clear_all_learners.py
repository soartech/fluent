import requests
import sys
import json

# IMPORTANT NOTE: Ruben has noted that we also need to delete the "activity_attempt_calculator.pkl" file, and should also restart the service after this is run.

lis_endpoint = "insertIPAddr/learner-inferences/learners"

# The object to overwrite the learner with.
patchObject = {
	"activityAttemptCounters" : [],
	"competencyAchievements" : [],
	"competencyAttemptCounters" : [],
	"goals" : [],
	"masteryEstimates" : [],
	"masteryProbabilities" : [],
	"pastGoals" : [],
	"pastMasteryEstimates" : [],
	"bored" : False,
	"confused" : False,
	"eureka" : False,
	"flow" : False,
	"frustrated" : False,
	"lastActivityHard" : False,
	"lastActivityUseful" : False,
	"sleepy" : False
}

def clear_all_learners(lis_endpoint):
	# Get the list of all users
	print("Getting Learners.")
	sys.stdout.flush()
	r = requests.get(lis_endpoint)
	learners = r.json()

	# Iterate through and clear each one
	for learner in learners:
		learner_id = learner["identifier"]
		#print(learner_id)
		clear_learner(learner_id, lis_endpoint)

def clear_learner(learner_id, lis_endpoint):
	print("Clearing Learner " + learner_id + "...")
	patchURL = lis_endpoint + "/" + learner_id

	# Grab the ETag for versioning
	r = requests.get(patchURL)
	etag = r.headers['ETag']

	# Patch the learner
	r = requests.patch(patchURL, json.dumps(patchObject), headers={ "Content-Type": "application/json", "If-Match": etag })
	print(r.text)


clear_all_learners(lis_endpoint)
