import logging
logger = logging.getLogger("flask-app")

from .base_processor import BaseMessageProcessor

class Topic2Processor(BaseMessageProcessor):
    def process_message(self, message_value: str):
        logger.info("Consumed message for pubsub2 = {message}".format(message = message_value))