"""This module provides telegram notifier configs."""

import os


NOTIFIER_INTERVAL = 10

# SQS stuff
SQS_MAX_MESSAGES = 10
SQS_QUEUE_NAME = "telegram-notifications"

# Telegram stuff
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# REDIS stuff
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
