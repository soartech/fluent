#!/usr/bin/env python
"""
Turn firehose on with "sudo rabbitmqctl trace_on before running script"
Turn firehose off with "sudo rabbitmqctl trace_off after any debugging session"
"""

from datetime import datetime
import pika

if __name__ == "__main__":

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    queue_name = "firehose"
    result = channel.queue_declare(queue=queue_name, exclusive=False)

    channel.queue_bind(exchange='amq.rabbitmq.trace',
                       queue=queue_name,
                       routing_key="#")

    print (' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(80*'=')
        print("[{0}] {1}:{2}:{3}:{4}".format(
            str(datetime.utcnow()),
            method.routing_key,
            properties.headers["node"],
            properties.headers["routing_keys"],
            body
        ))

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
