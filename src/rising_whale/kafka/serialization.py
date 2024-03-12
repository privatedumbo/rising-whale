import functools

from confluent_kafka import Message
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

from rising_whale.kafka.schema_registry import SchemaRegistryClient
from rising_whale.types import AvroModel


def _to_dict(obj: AvroModel, _: SerializationContext) -> dict:
    return obj.to_dict()


@functools.lru_cache
def _serializer_for_schema(
    schema_registry_client: SchemaRegistryClient, schema: str
) -> AvroSerializer:
    # This seems a bit redundant; we're working with abstractions around Confluent Kafka objects
    # As we don't expose `confluent_kafka.SchemaRegistryClient` we need to pass it like this.
    serializer = AvroSerializer(
        schema_registry_client=schema_registry_client.schema_registry_client,
        to_dict=_to_dict,
        schema_str=schema,
    )
    return serializer


@functools.lru_cache
def _deserializer_for_schema(
    schema_registry_client: SchemaRegistryClient, schema: str
) -> AvroDeserializer:
    avro_deserializer = AvroDeserializer(
        schema_registry_client=schema_registry_client,
        schema_str=schema,
    )
    return avro_deserializer


def serialize(schema_registry_client: SchemaRegistryClient, msg: AvroModel, topic: str) -> bytes:
    # This first call will avoid creating a new `AvroSerializer` if `settings` and `schema`
    # don't change
    serializer = _serializer_for_schema(
        schema_registry_client=schema_registry_client, schema=msg.avro_schema()
    )
    as_bytes = serializer(msg, ctx=SerializationContext(topic, MessageField.VALUE))
    return as_bytes


def deserialize(schema_registry_client: SchemaRegistryClient, msg: Message) -> AvroModel:
    content_as_bytes = msg.value()
    schema_id_from_msg = int.from_bytes(content_as_bytes[1:5])
    schema = schema_registry_client.get_schema(schema_id=schema_id_from_msg)
    deserializer = _deserializer_for_schema(
        schema_registry_client=schema_registry_client, schema=schema.schema_str
    )
    as_obj = deserializer(content_as_bytes, SerializationContext(msg.topic(), MessageField.VALUE))
    return as_obj
