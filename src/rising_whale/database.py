"""Database connection utils."""

from typing import TYPE_CHECKING, Optional

import psycopg2

if TYPE_CHECKING:
    from psycopg2 import connection

from rising_whale.settings import Settings, get_settings


def connect(settings: Settings) -> Optional["connection"]:
    """Return a connection to the underlying database."""
    conn = psycopg2.connect(
        database=settings.rising_wave_db_name,
        user=settings.rising_wave_db_username,
        host=settings.rising_wave_db_host,
        port=settings.rising_wave_db_port,
    )
    return conn


def execute(query: str) -> None:
    """Execute a given `query`."""
    settings = get_settings()
    conn = None
    try:
        conn = connect(settings)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
    finally:
        if conn:
            conn.close()
