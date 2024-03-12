from rising_whale.kafka.admin import AdminClient
from rising_whale.kafka.consumer import Consumer
from rising_whale.kafka.producer import Producer
from rising_whale.kafka.schema_registry import SchemaRegistryClient
from rising_whale.settings import get_settings
from rising_whale.types import Purchase

if __name__ == "__main__":
    topic = "rising-whale-input"  # Created manually from the console
    settings = get_settings()

    # Initializing objects
    admin_client = AdminClient(settings)
    registry_client = SchemaRegistryClient(settings)
    producer = Producer(settings)
    consumer = Consumer(settings=settings, topic=topic)
    msg = Purchase(purchase_id="purchase-abc123", items=2, price=5.0, venue_id="venue-123")

    # Create topic
    admin_client.create_topic(topic=topic)

    # Cleanup every time before reproducing e2e example
    registry_client.teardown()

    producer.send(topic=topic, msg=msg)

    schema = registry_client.get_latest_schema_for_topic(topic=topic)
    print(schema.schema.schema_str)

    msgs = consumer.poll()
    print(msgs)

    print(registry_client.schema_registry_client.get_subjects())
    print(registry_client.get_versions_for_subject("rising-whale-input-value"))
