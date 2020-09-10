"""This module provides functionality for cache interactions."""

from aiocache import Cache

from config import REDIS_HOST, REDIS_PORT


TELEGRAM_ID_CACHE_KEY = "telegram-id--{user_id}"
TELEGRAM_ID_CACHE_EXPIRE = 60 * 60 * 24 * 7  # 1 week

cache = Cache(Cache.REDIS, endpoint=REDIS_HOST, port=REDIS_PORT)
