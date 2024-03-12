from pyiceberg.catalog.sql import SqlCatalog

from rising_whale.settings import Settings


def _connect(settings: Settings) -> SqlCatalog:
    catalog = SqlCatalog(
        settings.catalog_name,
        **{
            "s3.endpoint": settings.catalog_s3_endpoint,
            "uri": settings.catalog_database_uri,
        },
    )
    return catalog


class IcebergClient:

    _catalog: SqlCatalog | None = None

    def __init__(self, settings: Settings):
        self._settings: Settings = settings

    @property
    def catalog(self) -> SqlCatalog:
        if not self._catalog:
            self._catalog = _connect(self._settings)

        return self._catalog
