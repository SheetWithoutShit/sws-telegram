"""This module is entrypoint for notifier service."""

import asyncio
import json
import logging

import aioboto3
import aiohttp

import config
from models import User
from errors import DatabaseError
from notifier.notifications import send_notification


LOGGER = logging.getLogger(__name__)


async def run_notifier():
    """Run processing SQS telegram notifications."""
    async with aioboto3.resource("sqs") as sqs, aiohttp.ClientSession() as aio_session:
        queue = await sqs.get_queue_by_name(QueueName=config.SQS_QUEUE_NAME)

        while True:
            messages = await queue.receive_messages({"MaxNumberOfMessages": config.SQS_MAX_MESSAGES})

            delete_tasks = []
            notifications_tasks = []
            for message in messages:
                delete_tasks.append(message.delete())

                try:
                    message_body = json.loads(await message.body)
                except json.JSONDecodeError as err:
                    LOGGER.error("Could not deserialize message body. Error: %s", err)
                    continue

                try:
                    text = message_body["text"]
                except KeyError:
                    LOGGER.error("Missed text field in message body: %s.", message_body)
                    continue

                telegram_id = message_body.get("telegram_id")
                user_id = message_body.get("user_id")
                if not user_id and telegram_id is None:
                    LOGGER.error("Missed user identifiers in message body: %s.", message_body)
                    continue

                if not telegram_id:
                    try:
                        telegram_id = await User.get_telegram_id(1)
                    except DatabaseError:
                        continue

                parse_mode = message_body.get("parse_mode", "markdown")
                disable_notification = message_body.get("disable_notification", True)

                notifications_tasks.append(send_notification(
                    aio_session=aio_session,
                    telegram_id=telegram_id,
                    text=text,
                    parse_mode=parse_mode,
                    disable_notification=disable_notification
                ))

            await asyncio.gather(*notifications_tasks, *delete_tasks)
            await asyncio.sleep(10)
