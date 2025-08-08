import pika
import ssl
import json

# RabbitMQ TLS connection settings
rabbitmq_host = "b-f2e4c804-d6cf-41ad-84a1-66c11dd91c1a.mq.us-east-1.on.aws"
rabbitmq_port = 5671
username = "queueadmin"
password = "r@bbitmQ232!"  # Replace with your real password
queue_name = "userdetails"

credentials = pika.PlainCredentials(username, password)

context = ssl.create_default_context(cafile="amazon_root_ca_1.pem")

parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host="/",
    ssl_options=pika.SSLOptions(context),
    credentials=credentials
)

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    # Here you could call OpenAI, transform the data, etc.

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f" [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C")
    channel.start_consuming()

except Exception as e:
    print("❌ Failed to connect or consume:", e)
