from database.db import db_connection


async def work_user(*args, part):
    async with await db_connection() as db:
        user_data = None

        if part == 'get':
            cursor = await db.execute("SELECT * FROM users WHERE tg_id = ?", (args[0],))
            user_data = await cursor.fetchone()
        elif part == 'create':
            first_name, role, tg_id = args
            await db.execute('''
                INSERT INTO users (first_name, role, tg_id)
                VALUES (?, ?, ?)
            ''', (first_name, role, tg_id))

        await db.commit()
        return user_data


async def work_faq(*args, part):
    async with await db_connection() as db:
        data_faq = None
        if part == 'get':
            cursor = await db.execute('SELECT * FROM faq;')
            data_faq = await cursor.fetchall()
        elif part == 'create':
            question, answer = args
            await db.execute('''
                INSERT INTO faq (question, answer)
                VALUES (?, ?)
            ''', (question, answer))
        elif part == 'delete':
            await db.execute('DELETE FROM faq WHERE faq_id = ?', (args[0], ))
        elif part == 'update':
            question, answer = args
            await db.execute('''
                UPDATE faq 
                SET quantity = ?
                    answer = ?
            ''', (question, answer))

        await db.commit()
        return data_faq


