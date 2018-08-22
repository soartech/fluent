#!/usr/bin/env python

import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import pika

application = Flask(__name__)


def log(response):
    time = datetime.now()
    # Output of print should end up in /var/log/apache2/statementforwarding.error.log
    print("[{}] - {}".format(str(time), response), flush=True)
        
AMQP_EXCHANGE = 'experiences'
AMQP_HOST = 'localhost'

class FanoutPublisher:
    def __init__(self, host, exchange_name):
        self._host = host
        self._exchange_name = exchange_name
        self._conn = None
        self._channel = None
        self._params = pika.connection.ConnectionParameters(host=self._host)
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
        log("Message sent: " + msg)

    def publish(self, msg):
        """Publish msg, reconnecting if necessary."""
        try:
            self._publish(msg)
        except pika.exceptions.ConnectionClosed:
            log('Reconnecting to queue')
            self.connect()
            self._publish(msg)

    def close(self):
        if self._conn and self._conn.is_open:
            log('Closing queue connection')
            self._conn.close()

publisher = FanoutPublisher(AMQP_HOST, AMQP_EXCHANGE)

@application.route('/')
def root():
    return 'Hello, world!'

@application.route('/hello')
def hello():
    return 'Hello, world!'

@application.route('/statementforwarding', methods=['PUT', 'POST'])
def webhook():
    if request.method == 'POST' or request.method == 'PUT':
        try:
            publisher.publish(json.dumps(request.json))
            return jsonify({'status': 'success ' + request.method}), 200
        except BaseException as e:
            log("Failed to publish message: " + json.dumps(request.json))
            log("Exception: " + str(e))

        return "Failed to publish message", 400

    else:
        log("Got an unexpected request method")
        return 'Got an unexpected request method', 400


if __name__ == '__main__':
    application.run(port=5678)
