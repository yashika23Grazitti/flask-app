import logging
logger = logging.getLogger("flask-app")

from abc import ABC, abstractmethod

class BaseMessageProcessor(ABC):
    @abstractmethod
    def process_message(self, message_value: str):
        pass