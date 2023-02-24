import logging
from flask import Flask
from motifer import FlaskLogFactory
from models.response import Response
from resources.admin import admin_blueprint

app = Flask(__name__)

# Initialize Motifer for log management.
factory = FlaskLogFactory(service="flask-app", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

# Register all the routes.
app.register_blueprint(admin_blueprint, url_prefix ='/api')

@app.route('/health', methods=['GET'])
def health():
    logger.debug("Flask app is running.")
    resp = Response(True, "Flask app is running!", None)
    return resp.to_dict()

if __name__ == "__main__":
    app.run(port=8080, debug=True)
