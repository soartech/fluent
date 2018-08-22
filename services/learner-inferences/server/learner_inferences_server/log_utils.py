import datetime

import json
from learner_inferences_server.lrs_utils import create_learner_inference_log_xapi, post_xapi_statement
#from learner_inferences_server.config import Config


class Config(object):
    LOG_TO_LRS = False
    LOG_XAPI_TO_FILE = True
    class LogLRSConfig(object):
        USR = "insertUsername"
        PWD = "insertPassword"
        HOST = "insertHost"
        PORT = "80"
        ENDPOINT = "data/xAPI/statements"

def print_with_time(msg):
    time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    print("[{}] - {}".format(str(time), msg), flush=True)

#def log_to_amqp(publisher, statement):
#    publisher.publish(json.dumps(statement))

def log_to_lrs(statement):
    lrs_url, usr, pwd = get_log_lrs_config()
    response = post_xapi_statement(statement, lrs_url, usr, pwd)
    return response

def get_log_lrs_config():
    lrs_url = '{0}:{1}/{2}'.format(Config.LogLRSConfig.HOST, Config.LogLRSConfig.PORT, Config.LogLRSConfig.ENDPOINT)
    usr = Config.LogLRSConfig.USR
    pwd = Config.LogLRSConfig.PWD
    return lrs_url, usr, pwd
