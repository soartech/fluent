#!/usr/bin/python3

import pika
import pika.exceptions
import json
from main import train_and_predict
from config import STUDY_ID
import daemon
import sys
import os
import signal
import lockfile
import daemon.pidfile
import argparse
import datetime

from config import AMQPConfig

dir_path = os.path.dirname(os.path.realpath(__file__))


def shutdown(signum, frame):
    sys.exit(0)


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
        print_with_time("INFO: Message Sent to Raw Inferences queue: {}".format(str(msg)))

    def publish(self, msg):
        """Publish msg, reconnecting if necessary."""
        try:
            self._publish(msg)
        except pika.exceptions.ConnectionClosed:
            print_with_time('WARN: Reconnecting to Raw Inferences queue...')
            self.connect()
            self._publish(msg)

    def close(self):
        if self._conn and self._conn.is_open:
            print_with_time("INFO: Closing Raw Inferences queue connection...")
            self._conn.close()


def init_daemon():
    with daemon.DaemonContext(stdout=sys.stdout,
                              stderr=sys.stdout,
                              working_directory=dir_path,
                              signal_map={
                                signal.SIGTERM: shutdown,
                                signal.SIGABRT: shutdown
                              },
                              pidfile=daemon.pidfile.PIDLockFile(dir_path+'/lock.pid')):

        #Process messages indefinitely or until KeyboardInterrupt error triggered.
        while True:
            try:
                publisher = FanoutPublisher(AMQPConfig.RawInferences.AMQP_HOST,
                                            AMQPConfig.RawInferences.AMQP_USR,
                                            AMQPConfig.RawInferences.AMQP_PWD,
                                            AMQPConfig.RawInferences.RAW_EXCHANGE_NAME)

                credentials = pika.PlainCredentials(username=AMQPConfig.Experiences.AMQP_USR, password=AMQPConfig.Experiences.AMQP_PWD)
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMQPConfig.Experiences.AMQP_HOST,
                                                                               credentials=credentials,
                                                                               connection_attempts=AMQPConfig.Experiences.CONNECTION_ATTEMPTS))
                channel = connection.channel()
                channel.exchange_declare(exchange=AMQPConfig.Experiences.AMQP_EXCHANGE, exchange_type='fanout')
                channel.queue_declare(queue=AMQPConfig.Experiences.AMQP_NAME, durable=True)
                channel.queue_bind(exchange=AMQPConfig.Experiences.AMQP_EXCHANGE, queue=AMQPConfig.Experiences.AMQP_NAME)

                def callback_func(ch, method, properties, body):
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    xapi_statement = json.loads(body.decode('utf-8').replace('&46;', '.'))
                    print_with_time('INFO: Received statement: {}'.format(xapi_statement['id']))
                    predictions = train_and_predict(STUDY_ID, [xapi_statement])
                    print_with_time('INFO: Prediction: {}'.format(str(predictions)))
                    if predictions is not None:
                        for pred in predictions:
                            try:
                                publisher.publish(json.dumps(pred))
                            except Exception as e:
                                print_with_time("ERROR: Exception when publishing prediction {}: {}".format(str(pred), str(e)))



                print_with_time("INFO: Waiting for messages...")
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(callback_func, queue=AMQPConfig.Experiences.AMQP_NAME)
                channel.start_consuming()
            except KeyboardInterrupt:
                print_with_time('WARN: KeyboardInterrupt detected while consuming messages. Stopping consumption...')
                raise # Should stop consuming messages at this point.
            except Exception as e:
                print_with_time('ERROR: Exception when consuming messages: {0}'.format(str(e)))
            finally:
                # Release resources before terminating thread or reconnecting.
                if channel and channel is not None:
                    channel.stop_consuming()
                if connection and connection is not None:
                    connection.close()
                if publisher and publisher is not None:
                    publisher.close()


def print_with_time(msg):
    time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    print("[{}] - {}".format(str(time), msg), flush=True)


parser = argparse.ArgumentParser(description='Start the evidence mapper AMQP listener.')
parser.add_argument('run_command', type=str, choices=['start', 'stop', 'restart'])
options = parser.parse_args()

if options.run_command == 'start':
    try:
        print_with_time('INFO: Starting service...')
        init_daemon()
    except lockfile.AlreadyLocked:
        print_with_time("INFO: Process already started. Use \'restart\' command instead.")
elif options.run_command == 'stop':
    try:
        print_with_time('INFO: Stopping service...')
        os.kill(int(open(dir_path + '/lock.pid').read()), signal.SIGTERM)
    except FileNotFoundError:
        print_with_time('WARN: File not found. Service is likely already stopped.')
    except ProcessLookupError:
        print_with_time('WARN: Process was not found. The lock file still exists, but the service does not. Deleting lock file...')
        os.remove(dir_path+'/lock.pid')
elif options.run_command == 'restart':
    try:
        print_with_time("INFO: Restarting service...")
        os.kill(int(open(dir_path + '/lock.pid').read()), signal.SIGTERM)
        init_daemon()
    except FileNotFoundError:
        print_with_time('WARN: File not found. Service is not running. Use \'start\' command instead.')
    except ProcessLookupError:
        print_with_time('WARN: Process was not found. The lock file still exists, but the service does not. Deleting lock file...')
        os.remove(dir_path+'/lock.pid')
        init_daemon()
