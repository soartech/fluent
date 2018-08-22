import cass_client
from cass_client.rest import ApiException

api = cass_client.CASSSingleObjectApi()

COMBAT_HUNTER_FRAMEWORK_ID = "59e884bb-510b-4f36-8443-8c3842336e28"
COMPETENCY_ID = "2fef4ebf-a526-4037-b9f4-fe53383db51a"
RELATION_ID = "81dd287a-dc04-4aa3-81f4-1cc132a58699"

try:
    framework = api.get_framework(framework_id=COMBAT_HUNTER_FRAMEWORK_ID)
    print('Combat hunter framework:\n{}\n{}'.format('=' * 40, framework))

    competency = api.get_competency(competency_id=COMPETENCY_ID)
    print('Example competency:\n{}\n{}'.format('=' * 40, competency))

    relation = api.get_relation(relation_id=RELATION_ID)
    print('Example relation:\n{}\n{}'.format('=' * 40, relation))


except  ApiException as e:
    print("Exception when calling MultiplerLearnersApi->get_learners: %s\n" % e)
