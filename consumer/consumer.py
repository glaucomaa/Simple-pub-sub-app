import pika
import json
import logging

logging.basicConfig(level=logging.INFO)

logging.info("started___________\n")
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue="data_queue")

channel.exchange_declare(exchange="dlx", exchange_type="direct")
channel.queue_declare(queue="dlq")

channel.queue_bind(exchange="dlx", queue="dlq", routing_key="")


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)

        value1 = data["value1"]
        value2 = data["value2"]
        oper = data["oper"]

        logging.info(f"Processed data: {value1} {oper} {value2} %s", data)
        if oper == "+":
            logging.info(f"\n answer: {value1+value2}\n")
        elif oper == "-":
            logging.info(f"\n answer: {value1-value2}\n")
        elif oper == "*":
            logging.info(f"\n answer: {value1*value2}\n")
        elif oper == "/":
            logging.info("Division detected")
            raise Exception("We don't do division")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error("Error processing message: %s\n", e)
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


channel.basic_consume(queue="data_queue", on_message_callback=callback)

logging.info("Consumer started. Waiting for messages...\n")
channel.start_consuming()
