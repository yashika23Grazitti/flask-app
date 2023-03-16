import logging
from pyconman import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

from abc import ABC, abstractmethod

class BaseMessageProcessor(ABC):
    @abstractmethod
    def process_message(self, message_value: str):
        pass