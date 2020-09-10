"""This module is entrypoint for telegram service."""

import os
import logging
import asyncio

import gino

from db import db, POSTGRES_DSN
from notifier.main import run_notifier


LOG_FORMAT = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"


def init_logging():
    """
    Initialize logging stream with info level to console and
    create file logger with info level if permission to file allowed.
    """
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    # disabling gino postgres echo logs
    # in order to set echo pass echo=True to db config dict
    logging.getLogger("gino.engine._SAEngine").propagate = False

    log_dir = os.environ.get("LOG_DIR")
    log_filepath = f"{log_dir}/telegram.log"
    if log_dir and os.path.isfile(log_filepath) and os.access(log_filepath, os.W_OK):
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logging.getLogger("").addHandler(file_handler)


async def main():
    """Runs bot and notifier services."""
    init_logging()

    engine = await gino.create_engine(POSTGRES_DSN)
    db.bind = engine

    await asyncio.gather(run_notifier())


if __name__ == '__main__':
    asyncio.run(main())
