#!/usr/bin/python3

import pika
import json
import daemon
import sys
import os
import signal
import lockfile
import argparse
import daemon.pidfile
import threading
import traceback

from learner_inferences_server.amqp_listener.inference_utils import process_raw_inference, process_experience
from learner_inferences_server.config import Config
from learner_inferences_server.log_utils import print_with_time, log_to_lrs
from learner_inferences_server.lrs_utils import create_learner_inference_log_xapi

dir_path = os.path.dirname(os.path.realpath(__file__))


class FanoutPublisher:
    def __init__(self, host, username, password, exchange_name):
        if username and password:
            credentials = pika.PlainCredentials(username=username,
                                                password=password)
        else:
            credentials = None

        self._host = host
        self._exchange_name = exchange_name
        self._conn = None
        self._channel = None
        self._params = pika.connection.ConnectionParameters(host=self._host, credentials=credentials)
        self.connect()

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()
            self._channel.exchange_declare(exchange=self._exchange_name, exchange_type='fanout')

    def _publish(self, msg):
        self._channel.basic_publish(exchange=self._exchange_name,
                                    routing_key='', #not used for fanout exchanges.
                                    body=msg,
                                    properties=pika.BasicProperties(delivery_mode=2))

    def publish(self, msg):
        """Publish msg, reconnecting if necessary."""
        try:
            self._publish(msg)
        except pika.exceptions.ConnectionClosed:
            self.connect()
            self._publish(msg)

    def close(self):
        if self._conn and self._conn.is_open:
            self._conn.close()



def shutdown(signum, frame):
    sys.exit(0)

def process_experiences():
    """Consume Experiences AMQP channel until KeyboardInterrupt detected."""

    def experience_callback_func(ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        statement = json.loads(body.decode('utf-8').replace('&46;', '.'))
        print_with_time('INFO: xAPI Statement received: {0}; verb: {1}'.format(statement['id'], statement['verb']['id']))
        process_experience(statement)

    while True:
        try:
            print_with_time('INFO: Connecting to Experiences AMQP channel...')
            connection = None
            credentials = pika.PlainCredentials(username=Config.AMQP.Experiences.AMQP_USR, password=Config.AMQP.Experiences.AMQP_PWD)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.AMQP.Experiences.AMQP_HOST,
                                                                           credentials=credentials,
                                                                           connection_attempts=Config.AMQP.Experiences.CONNECTION_ATTEMPTS))
            input_channel = connection.channel()
            input_channel.exchange_declare(exchange=Config.AMQP.Experiences.EXCHANGE_NAME, exchange_type='fanout')
            input_channel.queue_declare(queue=Config.AMQP.Experiences.QUEUE_NAME, durable=True)
            input_channel.queue_bind(exchange=Config.AMQP.Experiences.EXCHANGE_NAME, queue=Config.AMQP.Experiences.QUEUE_NAME)
            input_channel.basic_qos(prefetch_count=1)
            print_with_time('INFO: Connected to Experiences AMQP channel.')

            input_channel.basic_consume(experience_callback_func, queue=Config.AMQP.Experiences.QUEUE_NAME)
            print_with_time('INFO: Started listening for messages on Experiences Queue...')
            input_channel.start_consuming()
        except KeyboardInterrupt:
            print_with_time('WARN: KeyboardInterrupt detected while consuming Experiences. Stopping consumption...')
            raise # Should stop consuming messages at this point.
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
        finally:
            # Release resources before terminating thread or reconnecting.
            if input_channel and input_channel is not None:
                input_channel.stop_consuming()
            if connection and connection is not None:
                connection.close()

def process_raw_inferences():
    """Consume Raw Inferences AMQP channel until KeyboardInterrupt detected."""
    while True:
        try:
            print_with_time('INFO: Connecting to Raw Inferences AMQP channel...')
            credentials = pika.PlainCredentials(username=Config.AMQP.Inferences.AMQP_USR,
                                                password=Config.AMQP.Inferences.AMQP_PWD)
            connection = None
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.AMQP.Inferences.AMQP_HOST,
                                                                           port=Config.AMQP.Inferences.AMQP_PORT,
                                                                           credentials=credentials,
                                                                           connection_attempts=Config.AMQP.Inferences.CONNECTION_ATTEMPTS))
            input_channel = connection.channel()

            input_channel.exchange_declare(exchange=Config.AMQP.Inferences.RAW_EXCHANGE_NAME, exchange_type='fanout')
            input_channel.queue_declare(queue=Config.AMQP.Inferences.RAW_QUEUE_NAME, durable=True)
            input_channel.queue_bind(exchange=Config.AMQP.Inferences.RAW_EXCHANGE_NAME,
                                     queue=Config.AMQP.Inferences.RAW_QUEUE_NAME)

            outputPublisher = FanoutPublisher(Config.AMQP.Inferences.AMQP_HOST,
                                              Config.AMQP.Inferences.AMQP_USR,
                                              Config.AMQP.Inferences.AMQP_PWD,
                                              Config.AMQP.Inferences.DECONFLICTED_EXCHANGE_NAME)

            print_with_time('INFO: Connected to Raw Inferences AMQP channel.')

            def inference_callback_func(ch, method, properties, body):
                ch.basic_ack(delivery_tag=method.delivery_tag)

                raw_inference = json.loads(body.decode('utf-8').replace('&46;', '.'))

                print_with_time('INFO: Started processing raw inference: {0}'.format(raw_inference))
                received_statement = create_learner_inference_log_xapi(verb_id="https://w3id.org/xapi/dod-isd/verbs/received", verb_en_name="received",
                                                                       activity_id="insertIPAddr/receive-mastery-probability",
                                                                       activity_en_name="Receive Mastery Probability",
                                                                       obj_extensions={"insertIPAddr/learner-inferences/log-data": raw_inference},
                                                                       profile_id="https://w3id.org/xapi/dod-isd/v1.0")
                if Config.LOG_TO_LRS:
                    log_to_lrs(received_statement)
                if Config.LOG_XAPI_TO_FILE:
                    print_with_time("[XAPI LOG]: {}".format(json.dumps(received_statement)))

                learner_inferences = process_raw_inference(raw_inference)

                print_with_time('INFO: Result of processing raw inference: {0}'.format(learner_inferences))
                published_statement = create_learner_inference_log_xapi(verb_id="https://w3id.org/xapi/dod-isd/verbs/published", verb_en_name="published",
                                                                        activity_id="insertIPAddr/publish-learner-inference",
                                                                        activity_en_name="Publish Learner Inference",
                                                                        obj_extensions={"insertIPAddr/learner-inferences/log-data": learner_inferences},
                                                                        profile_id="https://w3id.org/xapi/dod-isd/v1.0")
                if Config.LOG_TO_LRS:
                    log_to_lrs(published_statement)
                if Config.LOG_XAPI_TO_FILE:
                    print_with_time("[XAPI LOG]: {}".format(json.dumps(published_statement)))

                if learner_inferences:  # Excludes empty dicts, and None
                    outputPublisher.publish(json.dumps(learner_inferences))

            input_channel.basic_qos(prefetch_count=1)
            input_channel.basic_consume(inference_callback_func, queue=Config.AMQP.Inferences.RAW_QUEUE_NAME)
            print_with_time('INFO: Started listening for messages on Raw Inferences Queue...')
            input_channel.start_consuming()
        except KeyboardInterrupt:
            print_with_time('WARN: KeyboardInterrupt detected while consuming Raw Inferences. Stopping consumption...')
            raise # Should stop consuming messages at this point.
        except Exception as e:
            print_with_time('ERROR: Exception when consuming Raw Inferences AMQP channel: {0}'.format(e))
            print(traceback.format_exc())
            pass
        finally:
            # Release resources before terminating thread or reconnecting.
            if input_channel and input_channel is not None:
                input_channel.stop_consuming()
            if connection and connection is not None:
                connection.close()

def init_daemon():
    with daemon.DaemonContext(stdout=sys.stdout,
                              stderr=sys.stdout,
                              working_directory=dir_path,
                              signal_map={
                                  signal.SIGTERM: shutdown,
                                  signal.SIGABRT: shutdown
                              },
                              pidfile=daemon.pidfile.PIDLockFile(dir_path+'/lock.pid')):

        experiences_threads = list()
        inferences_threads = list()
        try:
            # If issues when testing, look into:
            # https://stackoverflow.com/questions/24510310/consume-multiple-queues-in-python-pika?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
            experiences_threads = [threading.Thread(target=process_experiences) for i in range(Config.EXPERIENCES_THREADS)]
            for t in experiences_threads:
                t.start()

            inferences_threads = [threading.Thread(target=process_raw_inferences) for i in range(Config.INFERENCES_THREADS)]
            for t in inferences_threads:
                t.start()

        except KeyboardInterrupt:
            print_with_time('Closing on response to KeyboardInterrupt...')
            for t in experiences_threads:
                t.join(30)
            for t in inferences_threads:
                t.join(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the evidence mapper AMQP listener.')
    parser.add_argument('run_command', type=str, choices=['start', 'stop', 'restart'])
    options = parser.parse_args()

    if options.run_command == 'start':
        try:
            print_with_time('Starting service...')
            init_daemon()
        except lockfile.AlreadyLocked:
            print("Process already started. Use \'restart\' command instead.", flush=True)
    elif options.run_command == 'stop':
        try:
            print_with_time('Stopping service...')
            os.kill(int(open(dir_path + '/lock.pid').read()), signal.SIGTERM)
        except FileNotFoundError:
            print_with_time('File not found. Service is likely already stopped.')
        except ProcessLookupError:
            print_with_time('Process was not found. The lock file still exists, but the service does not. Deleting lock file...')
            os.remove(dir_path+'/lock.pid')
    elif options.run_command == 'restart':
        try:
            print("Restarting service...", flush=True)
            os.kill(int(open(dir_path + '/lock.pid').read()), signal.SIGTERM)
            init_daemon()
        except FileNotFoundError:
            print_with_time('File not found. Service is not running. Use \'start\' command instead.')
        except ProcessLookupError:
            print_with_time('Process was not found. The lock file still exists, but the service does not. Deleting lock file...')
            os.remove(dir_path+'/lock.pid')
            init_daemon()
