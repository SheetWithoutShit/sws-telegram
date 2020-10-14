"""Module that includes functionality to work with user data."""

import logging

from gino import exceptions
from sqlalchemy.exc import SQLAlchemyError

from db import db
from errors import DatabaseError
from cache import cache, TELEGRAM_ID_CACHE_EXPIRE, TELEGRAM_ID_CACHE_KEY


LOGGER = logging.getLogger(__name__)


class User:
    """Class that provides methods to work with User data."""

    SELECT_TELEGRAM_ID = db.text("""
        SELECT telegram_id
        FROM "user"
        WHERE id = :user_id and telegram_id is not null
    """)

    @classmethod
    async def get_telegram_id(cls, user_id):
        """Retrieve telegram id by user id."""
        telegram_id_cache_key = TELEGRAM_ID_CACHE_KEY.format(user_id=user_id)

        telegram_id = await cache.get(telegram_id_cache_key)
        if telegram_id:
            return telegram_id

        try:
            user = await db.one(cls.SELECT_TELEGRAM_ID, user_id=user_id)
        except exceptions.NoResultFound:
            LOGGER.error("Could not find user by id=%s with activated telegram.", user_id)
            raise DatabaseError
        except SQLAlchemyError as err:
            LOGGER.error("Failed to fetch user by id=%s. Error: %s", user_id, err)
            raise DatabaseError
        else:
            await cache.set(telegram_id_cache_key, user.telegram_id, TELEGRAM_ID_CACHE_EXPIRE)

        return user.telegram_id
