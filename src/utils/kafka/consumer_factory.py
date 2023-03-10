import logging
from configs.config_loader import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

from typing import List
from kafka import KafkaConsumer

from .base_processor import BaseMessageProcessor

class KafkaConsumerFactory:
    def __init__(self, bootstrap_servers: List[str], group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id

    def create_consumer(self, topic: str, message_processor: BaseMessageProcessor) -> KafkaConsumer:
        # logger.info(f"Creating consumer for topic {topic}")
        return KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: m.decode('utf-8') if m else None,
            key_deserializer=lambda m: m.decode('utf-8') if m else None
        ), message_processor