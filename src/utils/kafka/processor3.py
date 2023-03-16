import logging
from pyconman import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

from .base_processor import BaseMessageProcessor

class Topic3Processor(BaseMessageProcessor):
    def process_message(self, message_value: str):
        logger.info("Consumed message for pubsub3 = {message}".format(message = message_value))