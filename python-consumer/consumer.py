import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
import pika
import json
import ssl
import openai
import os
import logging
from dotenv import load_dotenv
from db import AIResponse, init_db, Session

init_db()
load_dotenv()  # loads from .env



client = openai.OpenAI()  # uses `OPENAI_API_KEY` from env automatically

def call_openai(payload):
    prompt = f"Please process this user input:\nName: {payload['name']}\nAge: {payload['age']}\nNumber: {payload['number']}\nReturn a short summary."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
logging.basicConfig(level=logging.INFO)
logging.info("Completed openai call")



def callback(ch, method, properties, body):
    try:
        print(f"[x] Received raw: {body}")
        data = json.loads(body)
        print(f"[x] Parsed: {data}")

        result = call_openai(data)
        print(f"[✓] OpenAI Response:\n{result}\n")

        # Save result to database
        session = Session()
        record = AIResponse(
            name=data['name'],
            age=data['age'],
            number=data['number'],
            response=result
        )
        session.add(record)
        session.commit()
        session.close()

        print("[✓] Saved to database.")
        logging.basicConfig(level=logging.INFO)
        logging.info("Saved to database.")


        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[!] Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        logging.basicConfig(level=logging.ERROR)
        logging.error("Problem uploading to db.")

# SSL context using AWS cert
context = ssl.create_default_context(cafile="amazon_root_ca_1.pem")

# Connection parameters
credentials = pika.PlainCredentials("queueadmin", "r@bbitmQ232!")
parameters = pika.ConnectionParameters(
    host="b-f2e4c804-d6cf-41ad-84a1-66c11dd91c1a.mq.us-east-1.on.aws",
    port=5671,
    virtual_host="/",
    credentials=credentials,
    ssl_options=pika.SSLOptions(context)
)

# Connect and consume
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="userdetails", durable=True)

print("[*] Waiting for messages... CTRL+C to exit")
channel.basic_consume(queue="userdetails", on_message_callback=callback)
channel.start_consuming()



