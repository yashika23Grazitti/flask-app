import logging
from configs.config_loader import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

from typing import List, Tuple

from kafka import KafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from .consumer_factory import KafkaConsumerFactory
from .base_processor import BaseMessageProcessor

class KafkaConsumerRunner:
    def __init__(self, consumer_factory: KafkaConsumerFactory, topics: List[Tuple[str, BaseMessageProcessor]], max_workers: int, server):
        self.consumer_factory = consumer_factory
        self.topics = topics
        self.max_workers = max_workers
        self.consumers = {}
        self.server = server

    def start_consumers(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for topic, message_processor in self.topics:
                consumer, processor = self.consumer_factory.create_consumer(topic, message_processor)
                self.consumers[topic] = consumer
                executor.submit(self._start_consumer, consumer, processor)

    def stop_consumers(self):
        for topic, consumer in self.consumers.items():
            consumer.close()
            
    def _start_consumer(self, consumer: KafkaConsumer, message_processor: BaseMessageProcessor):
        with self.server.app_context():
            try:
                for message in consumer:
                    message_processor.process_message(message.value)
            except Exception as e:
                print(f"Exception occurred while processing message: {str(e)}")