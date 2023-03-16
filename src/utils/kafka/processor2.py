import logging
from pyconman import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

from .base_processor import BaseMessageProcessor

class Topic2Processor(BaseMessageProcessor):
    def process_message(self, message_value: str):
        logger.info("Consumed message for pubsub2 = {message}".format(message = message_value))