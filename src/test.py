from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Tuple

from flask import Flask
from kafka import KafkaConsumer


class IMessageProcessor(ABC):
    @abstractmethod
    def process_message(self, message_value: str):
        pass


class KafkaConsumerFactory:
    def __init__(self, bootstrap_servers: List[str], group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id

    def create_consumer(self, topic: str, message_processor: IMessageProcessor) -> KafkaConsumer:
        return KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: m.decode('utf-8'),
            key_deserializer=lambda m: m.decode('utf-8')
        ), message_processor


class KafkaConsumerRunner:
    def __init__(self, consumer_factory: KafkaConsumerFactory, topics: List[Tuple[str, IMessageProcessor]], max_workers: int):
        self.consumer_factory = consumer_factory
        self.topics = topics
        self.max_workers = max_workers
        self.consumers = {}

    def start_consumers(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for topic, message_processor in self.topics:
                consumer, processor = self.consumer_factory.create_consumer(topic, message_processor)
                self.consumers[topic] = consumer
                executor.submit(self._start_consumer, consumer, processor)

    def stop_consumers(self):
        for topic, consumer in self.consumers.items():
            consumer.close()

    def _start_consumer(self, consumer: KafkaConsumer, message_processor: IMessageProcessor):
        for message in consumer:
            message_processor.process_message(message.value)


class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.consumer_runner = None

    def start(self):
        self.consumer_runner.start_consumers()
        self.app.run(debug=True)

    def stop(self):
        self.consumer_runner.stop_consumers()

    def add_route(self, rule: str, endpoint: str, view_func: Callable):
        self.app.add_url_rule(rule, endpoint, view_func)

    def set_consumer_runner(self, consumer_runner: KafkaConsumerRunner):
        self.consumer_runner = consumer_runner


class MyView:
    def __init__(self, message: str):
        self.message = message

    def index(self):
        return self.message


class MyMessageProcessor(IMessageProcessor):
    def process_message(self, message_value: str):
        print(f"Received message: {message_value}")


if __name__ == "__main__":
    kafka_bootstrap_servers = ['localhost:9093']
    kafka_group_id = 'my-group'
    kafka_consumer_factory = KafkaConsumerFactory(kafka_bootstrap_servers, kafka_group_id)

    topics = [
        ('pubsub1', MyMessageProcessor()),
        ('pubsub2', MyMessageProcessor()),
        ('pubsub3', MyMessageProcessor())
    ]

    consumer_runner = KafkaConsumerRunner(kafka_consumer_factory, topics, max_workers=len(topics))

    app = MyApp()
    app.set_consumer_runner(consumer_runner)

    view1 = MyView("Hello from view 1!")
    view2 = MyView("Hello from view 2!")

    app.add_route("/", "index1", view1.index)
    app.add_route("/", "index2", view2.index)

    try:
        app.start()
    finally:
        app.stop()
