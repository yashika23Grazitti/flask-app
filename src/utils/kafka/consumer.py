import logging, requests
logger = logging.getLogger("flask-app")
from kafka import KafkaConsumer

consumer = KafkaConsumer('my-topic', group_id='flask-group', bootstrap_servers=['localhost:9092'])
for msg in consumer:
    logger.info(msg)