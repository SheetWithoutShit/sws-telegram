"""This module provides telegram notifications interactions."""

import logging

from config import TELEGRAM_API


LOGGER = logging.getLogger(__name__)


async def send_notification(aio_session, telegram_id, text, parse_mode="markdown", disable_notification=True):
    """Send notification message to appropriated user."""
    send_message_url = f"{TELEGRAM_API}/sendMessage"
    send_message_params = {
        "chat_id": telegram_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_notification": str(disable_notification).lower()
    }

    async with aio_session.get(send_message_url, params=send_message_params) as response:
        response_json = await response.json()
        if not response_json["ok"]:
            LOGGER.error("A telegram notification was not delivered. Response: %s", response_json)
