"""This module provides functionality for database interactions."""

import os

import gino
from sqlalchemy.engine.url import URL

POSTGRES_DRIVER_NAME = "postgres"
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "swsuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sws")
POSTGRES_DSN = URL(
    drivername=POSTGRES_DRIVER_NAME,
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)

db = gino.Gino()
