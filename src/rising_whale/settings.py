import functools

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    # Postgres DB
    rising_wave_db_username: str
    rising_wave_db_name: str
    rising_wave_db_host: str
    rising_wave_db_port: int

    # Iceberg Catalog
    catalog_name: str
    catalog_s3_endpoint: str
    catalog_db_username: str
    catalog_db_password: str
    catalog_db_name: str
    catalog_db_host: str
    catalog_db_port: int

    # Redpanda Cluster
    redpanda_host: str
    redpanda_kafka_port: int
    redpanda_schema_registry_port: int

    @property
    def catalog_database_uri(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.catalog_db_username}:{self.catalog_db_password}@"
            f"{self.catalog_db_host}:{self.catalog_db_port}/"
            f"{self.catalog_db_name}"
        )

    @property
    def redpanda_bootstrap_server(self) -> str:
        return f"{self.redpanda_host}:{self.redpanda_kafka_port}"

    @property
    def redpanda_schema_registry_url(self) -> str:
        return f"http://{self.redpanda_host}:{self.redpanda_schema_registry_port}"


@functools.cache
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(settings)
