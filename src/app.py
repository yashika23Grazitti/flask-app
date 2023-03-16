import logging
import threading
import time, json
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
# from pyconman import ConfigLoader
from pyconman import ConfigLoader

# Load the configuration in the application scope.
config = ConfigLoader.get_config()

app = Flask(__name__)

# Initialize Motifer for log management.
factory = FlaskLogFactory(service=config.get(
    "service"), log_level=logging.DEBUG, server=app)
logger = factory.initialize()

# Register all the routes.
app.register_blueprint(admin_blueprint, url_prefix='/api')

json_config =json.dumps(config)
print(f"Final config JSON = {json_config}")

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
        kafka_bootstrap_servers = config["kafka"]["uri"]
        kafka_group_id = "flask-group"
        kafka_consumer_factory = KafkaConsumerFactory(
            kafka_bootstrap_servers, kafka_group_id)

        topics = [
            (config["kafka"]["topics"]["pubsub1"]["name"], Topic1Processor()),
            (config["kafka"]["topics"]["pubsub2"]["name"], Topic2Processor()),
            (config["kafka"]["topics"]["pubsub3"]["name"], Topic3Processor())
        ]

        consumer_runner = KafkaConsumerRunner(
            kafka_consumer_factory, topics, max_workers=len(topics), server=app)

        consumer_thread = threading.Thread(
            target=consumer_runner.start_consumers, name=config["kafka"]["thread_group"])
        consumer_thread.start()
        logger.info("Consumers were initialized successfully.")


if (config["kafka"]["enabled"] == True):
    init()
# Main section will not be called in Gunicorn.
# https://stackoverflow.com/questions/22260127/where-in-flask-gunicorn-to-initialize-application
if __name__ == "__main__":
    # init()
    app.run(port=8081, debug=True)
    # socketio = SocketIO(app)
    # socketio.run(app, debug=True)
