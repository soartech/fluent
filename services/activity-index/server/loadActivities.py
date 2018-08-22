import requests
import json
import sys
import os
from os import path
import activity_index_server.config as config
from pprint import pprint

# WARNING: a lot of things in this file are hardcoded
# This file will need to be updated when a change to the
# service's response or file directory structure is made


if len(sys.argv) != 2 or (sys.argv[1] != 'o' and sys.argv[1] != 'u'):
    print("Please provide one of the following two arguments:")
    print("'o' to overwrite existing metadata")
    print("'u' to update existing metadata")
    sys.exit()


directory = '../activity-data-entry/LearningActivity-metadata'
assessmentDirectory = directory + '/Assessment-metadata'
activityDirectory = directory + '/Activity-metadata'
selfReportDirectory = directory + '/SelfReport-metadata'
basePath = path.dirname(__file__)

url = config.Config.ACTIVITY_ENDPOINT
header = {"Content-type": "application/json"}

fileToIdDict = {}


# For every JSON file in the assessment directory...
for fileName in os.listdir(assessmentDirectory):
    if not fileName.endswith(".json"):
        continue
    
    filePath = path.abspath(path.join(basePath, assessmentDirectory, fileName))
    with open(filePath, encoding='utf-8') as jsonFile:
        # ...load it...
        jsonData = json.load(jsonFile)
        jsonData['metadataFile'] = fileName
        
        # ...shave off each competency version number...
        alignments = jsonData['educationalAlignment']
        for i in range(len(alignments)):
            if 'targetUrl' in alignments[i]:
                alignmentUrl = alignments[i]['targetUrl']
                urlComponents = alignmentUrl.split('/')
                if len(urlComponents) >= 3 and 'Competency' in urlComponents[-3]:
                    slashIndex = alignmentUrl.rfind('/')
                    alignments[i]['targetUrl'] = alignmentUrl[:slashIndex]
        
        # ...send it as part of a post or patch request to the server...
        if sys.argv[1] == 'o':
            response = requests.post(url, headers = header, data = json.dumps(jsonData))
        elif sys.argv[1] == 'u':
            response = requests.patch(url + '/' + fileName, headers = header, data = json.dumps(jsonData))
        print(response.text)
        
        # ...and store the ID of the new assessment into the file->ID dictionary
        fileToIdDict[fileName] = url + '/' + response.text[-26:-2]


# For every JSON file in the activity directory...
for fileName in os.listdir(activityDirectory):
    if not fileName.endswith(".json"):
        continue
    
    filePath = path.abspath(path.join(basePath, activityDirectory, fileName))
    with open(filePath, encoding='utf-8') as jsonFile:
        # ...load it...
        jsonData = json.load(jsonFile)
        jsonData['metadataFile'] = fileName
        
        # ...give the activity a reference to its assessment and shave off each competency version number...
        alignments = jsonData['educationalAlignment']
        for i in range(len(alignments)):
            if 'additionalType' in alignments[i] and alignments[i]['additionalType'] == 'AppropriateAssessmentAlignment':
                if 'targetUrl' in alignments[i]:
                    assessmentFile = alignments[i]['targetUrl'][1:-1]
                    if assessmentFile in fileToIdDict:
                        jsonData['educationalAlignment'][i]['targetUrl'] = fileToIdDict[assessmentFile]
            if 'targetUrl' in alignments[i]:
                alignmentUrl = alignments[i]['targetUrl']
                urlComponents = alignmentUrl.split('/')
                if len(urlComponents) >= 3 and 'Competency' in urlComponents[-3]:
                    slashIndex = alignmentUrl.rfind('/')
                    alignments[i]['targetUrl'] = alignmentUrl[:slashIndex]

        # ...and send it as part of a post or patch request to the server
        if sys.argv[1] == 'o':
            response = requests.post(url, headers = header, data = json.dumps(jsonData))
        elif sys.argv[1] == 'u':
            response = requests.patch(url + '/' + fileName, headers = header, data = json.dumps(jsonData))
        print(response.text)

# For the JSON file in the self-report directory...
for fileName in os.listdir(selfReportDirectory):
    if not fileName.endswith(".json"):
        continue
    
    filePath = path.abspath(path.join(basePath, selfReportDirectory, fileName))
    with open(filePath, encoding='utf-8') as jsonFile:
        # ...load it...
        jsonData = json.load(jsonFile)
        jsonData['metadataFile'] = fileName

        # ...and send it as part of a post or patch request to the server
        if sys.argv[1] == 'o':
            response = requests.post(url, headers = header, data = json.dumps(jsonData))
        elif sys.argv[1] == 'u':
            response = requests.patch(url + '/' + fileName, headers = header, data = json.dumps(jsonData))
        print(response.text)

# Generate mappings from TLOs/ELOs and token types to their associated activities
url = config.Config.ASSOCIATIONS_ENDPOINT
response = requests.post(url)
print(response.text)
