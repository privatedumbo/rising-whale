from confluent_kafka.admin import AdminClient as KafkaAdminClient
from confluent_kafka.admin import NewTopic

from rising_whale.settings import Settings


def kafka_admin_settings(settings: Settings) -> dict:
    return {
        "bootstrap.servers": settings.redpanda_bootstrap_server,
    }


class AdminClient:

    _client: KafkaAdminClient | None = None

    def __init__(self, settings: Settings):
        self._settings: Settings = settings

    @property
    def client(self) -> KafkaAdminClient:
        if not self._client:
            self._client = KafkaAdminClient(kafka_admin_settings(self._settings))
        return self._client

    def create_topic(self, topic: str) -> None:
        self.client.create_topics(
            [
                NewTopic(topic, 1, 1),
            ]
        )
