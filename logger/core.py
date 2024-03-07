from pathlib import Path
from .database import connect_db
from datetime import datetime

from aiosqlite import Connection

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = f'{BASE_DIR}/db.sqlite3'


@connect_db(DB_PATH)
async def init_tables(db: Connection):
    await db.execute('CREATE TABLE IF NOT EXISTS info_logs(user TEXT, method TEXT, path TEXT, date TEXT, status_code INTEGER);')
    await db.execute('CREATE TABLE IF NOT EXISTS error_logs(user TEXT, method TEXT, path TEXT, date TEXT, status_code INTEGER, detail TEXT);')
    await db.commit()


@connect_db(DB_PATH)
async def log_info(db: Connection, user: str, method: str, path: str, status_code: int):
    date = datetime.now()
    await db.execute(f"INSERT INTO info_logs VALUES ('{user}', '{method}', '{path}', '{date}', {status_code});")
    await db.commit()


@connect_db(DB_PATH)
async def log_error(db: Connection, user: str, method: str, path: str, status_code: int, detail: str):
    date = datetime.now()
    await db.execute(f"INSERT INTO error_logs VALUES ('{user}', '{method}', '{path}', '{date}', {status_code}, '{detail}');")
    await db.commit()
