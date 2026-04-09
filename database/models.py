import asyncio
from database.db import db_connection


async def create_table_users():
    async with db_connection() as db:
        await db.executescript('''
            DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                role TEXT DEFAULT "client",
                tg_id BIGINT NOT NULL UNIQUE
            );
        ''')
        await db.commit()


async def create_table_faq():
    async with db_connection() as db:
        await db.executescript('''
            DROP TABLE IF EXISTS faq;
            CREATE TABLE IF NOT EXISTS faq(
                faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT
            );
        ''')
        await db.commit()


async def start_create_models():
    await create_table_users()
    await create_table_faq()


if __name__ == '__main__':
    asyncio.run(start_create_models())
