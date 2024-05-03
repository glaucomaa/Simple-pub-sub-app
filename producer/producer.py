import pika
import json
import time
import random
import logging

logging.basicConfig(level=logging.INFO)


def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            channel = connection.channel()
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.error("Failed to connect to RabbitMQ: %s\n", e)
            time.sleep(5)  


def send_data_to_queue(channel, data):
    try:
        channel.basic_publish(
            exchange="", routing_key="data_queue", body=json.dumps(data)
        )
        logging.info(
            f"Sent data:< {data['value1']} {data['oper']} {data['value2']} >%s", data
        )
    except pika.exceptions.AMQPConnectionError as e:
        logging.error("Failed to send data to RabbitMQ: %s", e)
        raise


def main():
    connection, channel = connect_to_rabbitmq()

    channel.queue_declare(queue="data_queue")

    while True:
        try:
            oper = ["+", "-", "*", "+", "-", "*", "+", "-", "*", "/"]
            data = {
                "value1": random.randint(1, 100),
                "value2": random.randint(1, 100),
                "oper": random.choice(oper),
            }

            if random.random() < 0.1:
                logging.info("Sending message to DLQ due to probability\n")
                send_data_to_queue(channel, data)
                raise Exception("Message intentionally sent to DLQ")

            send_data_to_queue(channel, data)

            time.sleep(5)
        except Exception as e:
            logging.error("Error occurred: %s", e)
            try:
                channel.basic_publish(exchange="", routing_key="dlq", body=str(e))
                logging.info("Sent error to DLQ: %s", e)
            except pika.exceptions.AMQPConnectionError as e:
                logging.error("Failed to send error to DLQ: %s", e)


if __name__ == "__main__":
    main()
