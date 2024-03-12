from typing import Iterator

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaException
from dataclasses_avroschema import AvroModel

from rising_whale.kafka.schema_registry import SchemaRegistryClient
from rising_whale.kafka.serialization import deserialize
from rising_whale.settings import Settings

_auto_offset_reset = "earliest"
_group_id = "default"


def kafka_consumer_settings(settings: Settings) -> dict:
    return {
        "bootstrap.servers": settings.redpanda_bootstrap_server,
        "auto.offset.reset": _auto_offset_reset,
        "group.id": _group_id,
    }


class Consumer:

    _consumer: KafkaConsumer | None = None
    _schema_registry_client: SchemaRegistryClient | None = None

    def __init__(self, settings: Settings, topic: str):
        self._settings: Settings = settings
        self.topic = topic

    @property
    def consumer(self) -> KafkaConsumer:
        if not self._consumer:
            self._consumer = KafkaConsumer(kafka_consumer_settings(self._settings))
            self._consumer.subscribe(topics=[self.topic])
        return self._consumer

    @property
    def schema_registry_client(self) -> SchemaRegistryClient:
        if not self._schema_registry_client:
            self._schema_registry_client = SchemaRegistryClient(self._settings)
        return self._schema_registry_client

    def poll(self) -> Iterator[AvroModel]:
        while True:
            try:
                # SIGINT can't be handled when polling, limit timeout to 1 second.
                msg = self.consumer.poll(1.0)
                if not msg:
                    continue
                elif msg.error():
                    raise KafkaException(msg.error())

                obj = deserialize(
                    schema_registry_client=self.schema_registry_client,
                    msg=msg,
                )
                yield obj

            except KeyboardInterrupt:
                break

        self.consumer.close()
