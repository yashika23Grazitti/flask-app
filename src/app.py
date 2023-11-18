import logging
import threading
import time, json
from flask import Flask
# from flask_socketio import SocketIO
from motifer import FlaskLogFactory
from models.response import Response
from resources.admin import admin_blueprint
# Kafka consumers
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
    resp = Response(True, "Flask app is running! through jenkins on port 5000", None)
    return resp.to_dict()


# Main section will not be called in Gunicorn.
# https://stackoverflow.com/questions/22260127/where-in-flask-gunicorn-to-initialize-application
if __name__ == "__main__":
    # init()
    app.run(port=8081, debug=True)
    # socketio = SocketIO(app)
    # socketio.run(app, debug=True)
