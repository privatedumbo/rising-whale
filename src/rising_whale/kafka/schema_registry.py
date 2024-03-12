from confluent_kafka.schema_registry import RegisteredSchema, Schema
from confluent_kafka.schema_registry import SchemaRegistryClient as KafkaSchemaRegistryClient

from rising_whale.settings import Settings


def schema_registry_client_settings(settings: Settings) -> dict:
    return {"url": settings.redpanda_schema_registry_url}


def subject_name_for_topic(topic: str) -> str:
    return f"{topic}-value"


class SchemaRegistryClient:

    _client: KafkaSchemaRegistryClient | None = None

    def __init__(self, settings: Settings):
        self._settings: Settings = settings

    @property
    def schema_registry_client(self) -> KafkaSchemaRegistryClient:
        if not self._client:
            self._client = KafkaSchemaRegistryClient(
                schema_registry_client_settings(self._settings)
            )
        return self._client

    def get_schema(self, schema_id: int) -> Schema:
        return self.schema_registry_client.get_schema(schema_id=schema_id)

    def get_subjects(self) -> list[str]:
        return self.schema_registry_client.get_subjects()

    def get_versions_for_subject(self, subject: str) -> list[int]:
        return self.schema_registry_client.get_versions(subject)

    def get_latest_schema_for_topic(self, topic: str) -> RegisteredSchema:
        subject = subject_name_for_topic(topic)
        return self.schema_registry_client.get_latest_version(subject_name=subject)

    def teardown(self) -> None:
        subjects = self.schema_registry_client.get_subjects()
        for s in subjects:
            self.schema_registry_client.delete_subject(s, permanent=True)
