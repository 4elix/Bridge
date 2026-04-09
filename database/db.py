import aiosqlite
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def db_connection():
    return aiosqlite.connect(DB_PATH)
