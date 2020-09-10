"""This module is entrypoint for telegram service."""

import asyncio

import gino

from db import db, POSTGRES_DSN
from notifier.main import run_notifier


async def main():
    """Runs bot and notifier services."""
    engine = await gino.create_engine(POSTGRES_DSN)
    db.bind = engine

    await asyncio.gather(run_notifier())


if __name__ == '__main__':
    asyncio.run(main())
