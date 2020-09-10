"""This module is entrypoint for notifier service."""

import asyncio
import json
import logging

import aioboto3
import aiohttp

import config
from models import User
from errors import SWSDatabaseError
from notifier.notifications import send_notification


LOGGER = logging.getLogger(__name__)


async def run_notifier():
    """Run processing SQS telegram notifications."""
    async with aioboto3.resource("sqs") as sqs:
        queue = await sqs.get_queue_by_name(QueueName=config.SQS_QUEUE_NAME)
        await queue.send_message(MessageBody=(json.dumps({"user_id": 3, "text": "test```test```"})))
        aio_session = aiohttp.ClientSession()

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
                    user_id = message_body["user_id"]
                    text = message_body["text"]
                except KeyError:
                    LOGGER.error("Missed required fields in message body: %s.", message_body)

                parse_mode = message_body.get("parse_mode", "markdown")
                disable_notification = message_body.get("disable_notification", True)

                try:
                    telegram_id = await User.get_telegram_id(user_id)
                except SWSDatabaseError:
                    continue

                notifications_tasks.append(send_notification(
                    aio_session=aio_session,
                    telegram_id=telegram_id,
                    text=text,
                    parse_mode=parse_mode,
                    disable_notification=disable_notification
                ))

            await asyncio.gather(*notifications_tasks, *delete_tasks)
            await aio_session.close()
            await asyncio.sleep(10)
