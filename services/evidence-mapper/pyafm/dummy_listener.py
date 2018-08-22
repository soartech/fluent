#!/usr/bin/python3

import pika
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


dir_path = os.path.dirname(os.path.realpath(__file__))


def shutdown(signum, frame):
    sys.exit(0)


def init_daemon():
    with daemon.DaemonContext(stdout=sys.stdout,
                              stderr=sys.stderr,
                              working_directory=dir_path,
                              signal_map={
                                signal.SIGTERM: shutdown,
                                signal.SIGABRT: shutdown
                              },
                              pidfile=daemon.pidfile.PIDLockFile(dir_path+'/dummy_lock.pid')):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        def callback_func(ch, method, properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(body)

        channel.queue_declare(queue='test_pub')
        print("Waiting for messages")
        channel.basic_consume(callback_func, queue='test_pub')
        channel.start_consuming()

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

        connection.close()


parser = argparse.ArgumentParser(description='Start the dummy AMQP listener.')
parser.add_argument('run_command', type=str, choices=['start', 'stop', 'restart'])
options = parser.parse_args()

if options.run_command == 'start':
    try:
        print('Starting service...')
        init_daemon()
    except lockfile.AlreadyLocked:
        print("Process already started. Use \'restart\' command instead.")
elif options.run_command == 'stop':
    try:
        print('Stopping service...')
        os.kill(int(open(dir_path + '/dummy_lock.pid').read()), signal.SIGTERM)
    except FileNotFoundError:
        print('File not found. Service is likely already stopped.')
    except ProcessLookupError:
        print('Process was not found. The lock file still exists, but the service does not. Deleting lock file...')
        os.remove(dir_path+'/dummy_lock.pid')
elif options.run_command == 'restart':
    try:
        print("Restarting service...")
        os.kill(int(open(dir_path + '/dummy_lock.pid').read()), signal.SIGTERM)
        init_daemon()
    except FileNotFoundError:
        print('File not found. Service is not running. Use \'start\' command instead.')
    except ProcessLookupError:
        print('Process was not found. The lock file still exists, but the service does not. Deleting lock file...')
        os.remove(dir_path+'/dummy_lock.pid')
        init_daemon()
