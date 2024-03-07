from functools import wraps
import aiosqlite
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def connect_db(db_url):
    def decorator(func):
        wraps(func)

        async def wrapper(*args, **kwargs):
            async with aiosqlite.connect(db_url) as db:
                return await func(db, *args, **kwargs)

        return wrapper

    return decorator

