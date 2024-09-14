#!/usr/bin/env python
import pika
import sys

import pika

# Define the connection parameters (change as per your RabbitMQ setup)
connection_params = pika.ConnectionParameters('rabbitmq')

# Establish connection
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare the direct exchange named 'data_process'
channel.exchange_declare(exchange='data_process', exchange_type='direct')

# Declare the queue
queue_name = 'data_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Bind the queue to the exchange with a routing key
routing_key = 'data_key'
channel.queue_bind(exchange='data_process', queue=queue_name, routing_key=routing_key)

# Print success message
print(f"Queue '{queue_name}' bound to exchange 'data_process' with routing key '{routing_key}'.")
message = ' '.join(sys.argv[1:]) or "info: No data!"
channel.basic_publish(exchange='data_process', routing_key=routing_key, body=message)
print(f" [x] Sent {message}")
# Close the connection
connection.close()