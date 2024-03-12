# Rising Whale

Playing around with Streaming and Rising Wave

## Quickstart

### Project setup

This project is managed through invoke.
```shell
$ poetry install
$ inv --list
```

and serve yourself :)

### Setting up Rising Wave

```shell
$ cd docker
$ docker-compose up --build -d
```

After this, you should be able to access:
* Rising Wave UI: http://127.0.0.1:5691/
* Grafana: http://127.0.0.1:3001/
* Minio: http://127.0.0.1:9400/
  * Username: `hummockadmin`
  * Password: `hummockadmin`
* Prometheus: http://127.0.0.1:9500/
* Redpanda Console: http://127.0.0.1:8080/

And connect to a local postgres instance with the arguments in `.env` suffixed with `RISING_WAVE`.

### Example setup

I'm assuming you already configured Rising Wave following the previous step!

As this in still under active development, there is not a single neat clean tidy entrypoint/CLI for this.

```shell
$ python src/rising_whale/kafka/main.py
```

After running this:
1) You should have 1 topic created
2) You should have 1 message in the topic
3) The message's schema should be registered in RedPanda schema registry

Next:
1) Connect to RisingWave database through your favorite SQL Client
2) Allow Rising Wave to read from the topic and query from it:

```sql
CREATE SOURCE IF NOT EXISTS rising_whale_purchase
WITH (
   connector='kafka',
   topic='rising-whale-input',
   properties.bootstrap.server='message_queue:29092',
) FORMAT PLAIN ENCODE AVRO (
   schema.registry = 'http://message_queue:8081'
);

select *, _rw_kafka_timestamp from rising_whale_purchase;
```
