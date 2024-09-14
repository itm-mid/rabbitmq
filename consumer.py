#!/usr/bin/env python
import pika
import time

# Set up the connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare the queue to ensure it exists
queue_name = 'data_queue'
channel.queue_declare(queue=queue_name, durable=True)
channel.basic_qos(prefetch_count=10)

# Define the callback function to process messages
def callback(ch, method, properties, body):
    message = body.decode()  # Decode the message to a string
    try:
        # Attempt to convert the message to an integer and add 1
        processed_message = int(message) + 1
        time.sleep(5)
        print(f" [x] Received and processed message: {processed_message}")
    except ValueError:
        # Handle the case where the message is not a number
        print(f" [x] Received non-numeric message: '{message}'")
    
    # Acknowledge that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up the consumer to listen to the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')

# Start consuming messages
channel.start_consuming()
