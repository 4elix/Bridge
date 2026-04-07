import aiosqlite

DB_PATH = 'database/database.db'


async def db_connection():
    return await aiosqlite.connect(DB_PATH)
