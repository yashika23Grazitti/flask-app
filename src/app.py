import logging
import threading
import time
from flask import Flask
# from flask_socketio import SocketIO
from motifer import FlaskLogFactory
from models.response import Response
from resources.admin import admin_blueprint
# Kafka consumers
from utils.kafka.consumer_factory import KafkaConsumerFactory
from utils.kafka.runner import KafkaConsumerRunner
from utils.kafka.processor1 import Topic1Processor
from utils.kafka.processor2 import Topic2Processor
from utils.kafka.processor3 import Topic3Processor

# topics = ['pubsub', 'pubsub1', 'pubsub2', 'pubsub3', 'pubsub4']

app = Flask(__name__)

# Initialize Motifer for log management.
factory = FlaskLogFactory(service="flask-app", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

# Register all the routes.
app.register_blueprint(admin_blueprint, url_prefix='/api')


@app.route('/health', methods=['GET'])
def health():
    # time.sleep(5)
    logger.debug("Flask app is running.")
    resp = Response(True, "Flask app is running!", None)
    return resp.to_dict()


def init():
    with app.app_context():
        # Initialize all the consumers
        logger.info("Initialize all the consumers.")
        kafka_bootstrap_servers = ['localhost:9093']
        kafka_group_id = "flask-group"
        kafka_consumer_factory = KafkaConsumerFactory(kafka_bootstrap_servers, kafka_group_id)

        topics = [
            ('pubsub1', Topic1Processor()),
            ('pubsub2', Topic2Processor()),
            ('pubsub3', Topic3Processor())
        ]

        consumer_runner = KafkaConsumerRunner(kafka_consumer_factory, topics, max_workers=len(topics), server=app)

        consumer_thread = threading.Thread(target=consumer_runner.start_consumers, name="consumer")
        consumer_thread.start()
        logger.info("Consumers were initialized successfully.")


if __name__ == "__main__":
    init()
    app.run(port=8080, debug=True)
    # socketio = SocketIO(app)
    # socketio.run(app, debug=True)
