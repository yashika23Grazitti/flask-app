import logging
logger = logging.getLogger("flask-app")
from kafka import KafkaConsumer

# pubsub_consumer = KafkaConsumer('pubsub', group_id='flask-group', bootstrap_servers=['localhost:9093'])
# pubsub1_consumer = KafkaConsumer('pubsub1', group_id='flask-group', bootstrap_servers=['localhost:9093'])
# pubsub2_consumer = KafkaConsumer('pubsub2', group_id='flask-group', bootstrap_servers=['localhost:9093'])
# pubsub3_consumer = KafkaConsumer('pubsub3', group_id='flask-group', bootstrap_servers=['localhost:9093'])
# pubsub4_consumer = KafkaConsumer('pubsub4', group_id='flask-group', bootstrap_servers=['localhost:9093'])

def pubsub_consumer():
    print("Consumer initalized pubsub_consumer")
    pubsub_consumer = KafkaConsumer('pubsub', group_id='flask-group', bootstrap_servers=['localhost:9093'])
    for msg in pubsub_consumer:
        print("*** pubsub *** Kakfa message consumed.")
        # print(msg)
        print(msg.value)

def pubsub1_consumer():
    print("Consumer initalized pubsub1_consumer")
    pubsub1_consumer = KafkaConsumer('pubsub1', group_id='flask-group', bootstrap_servers=['localhost:9093'])
    for msg in pubsub1_consumer:
        print("*** pubsub1 *** Kakfa message consumed.")
        # print(msg)
        print(msg.value)

def pubsub2_consumer():
    print("Consumer initalized pubsub2_consumer")
    pubsub2_consumer = KafkaConsumer('pubsub2', group_id='flask-group', bootstrap_servers=['localhost:9093'])
    for msg in pubsub2_consumer:
        print("*** pubsub2 *** Kakfa message consumed.")
        # print(msg)
        print(msg.value)

def pubsub3_consumer():
    print("Consumer initalized pubsub3_consumer")
    pubsub3_consumer = KafkaConsumer('pubsub4', group_id='flask-group', bootstrap_servers=['localhost:9093'])
    for msg in pubsub3_consumer:
        print("*** pubsub3 *** Kakfa message consumed.")
        # print(msg)
        print(msg.value)

def pubsub4_consumer():
    print("Consumer initalized pubsub4_consumer")
    pubsub4_consumer = KafkaConsumer('pubsub4', group_id='flask-group', bootstrap_servers=['localhost:9093'])
    for msg in pubsub4_consumer:
        print("*** pubsub4 *** Kakfa message consumed.")
        # print(msg)
        print(msg.value)