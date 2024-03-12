from confluent_kafka import Producer as KafkaProducer
from dataclasses_avroschema import AvroModel

from rising_whale.kafka.schema_registry import SchemaRegistryClient
from rising_whale.kafka.serialization import serialize
from rising_whale.settings import Settings

_codec = "utf-8"


def kafka_producer_settings(settings: Settings) -> dict:
    return {
        "bootstrap.servers": settings.redpanda_bootstrap_server,
    }


class Producer:

    _producer: KafkaProducer | None = None
    _schema_registry_client: SchemaRegistryClient | None = None

    def __init__(self, settings: Settings):
        self._settings: Settings = settings

    @property
    def producer(self) -> KafkaProducer:
        if not self._producer:
            self._producer = KafkaProducer(kafka_producer_settings(self._settings))
        return self._producer

    @property
    def schema_registry_client(self) -> SchemaRegistryClient:
        if not self._schema_registry_client:
            self._schema_registry_client = SchemaRegistryClient(self._settings)
        return self._schema_registry_client

    def send(self, topic: str, msg: AvroModel) -> None:
        serialized_value = serialize(
            schema_registry_client=self.schema_registry_client,
            msg=msg,
            topic=topic,
        )
        self.producer.produce(
            topic=topic,
            value=serialized_value,
        )
        self.producer.flush()
