"""
To be run on the same server where Experiences AMQP service is running, for debugging purposes.

Turn AMQP firehose on with "sudo rabbitmqctl trace_on" before using this script.
Turn AMQP firehose off with "sudo rabbitmqctl trace_off" after using this script.
"""

import pika
import json

if __name__ == "__main__":

    credentials = pika.PlainCredentials(username="insertUsername",
                                        password="insertPassword")
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='insertHost',  # Replace with localhost if running on the LRS VM itself
        credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange="experiences", exchange_type='fanout')
    result = channel.queue_declare(durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="experiences", queue=queue_name)


    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(40*'=')
        print(json.dumps(json.loads(body.decode('utf-8')), indent=4))

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
