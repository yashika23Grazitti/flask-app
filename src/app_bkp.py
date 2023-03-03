import logging, threading, time
from flask import Flask
from motifer import FlaskLogFactory
from models.response import Response
from resources.admin import admin_blueprint
# Kafka consumers
from utils.kafka.consumer import pubsub_consumer, pubsub1_consumer, pubsub2_consumer, pubsub3_consumer, pubsub4_consumer

topics = ['pubsub', 'pubsub1', 'pubsub2', 'pubsub3', 'pubsub4']

app = Flask(__name__)

# Initialize Motifer for log management.
factory = FlaskLogFactory(service="flask-app", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

# Initialize all the consumers
# pubsub_consumer()

# Register all the routes.
app.register_blueprint(admin_blueprint, url_prefix='/api')


@app.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    logger.debug("Flask app is running.")
    resp = Response(True, "Flask app is running!", None)
    return resp.to_dict()


@app.before_first_request
def init():
    # Initialize all the consumers
    # pubsub_consumer()
    thread1 = threading.Thread(target=pubsub_consumer)
    thread2 = threading.Thread(target=pubsub1_consumer)
    thread3 = threading.Thread(target=pubsub2_consumer)
    thread4 = threading.Thread(target=pubsub3_consumer)
    thread5 = threading.Thread(target=pubsub4_consumer)
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()


if __name__ == "__main__":
    app.run(port=8080, debug=True)
