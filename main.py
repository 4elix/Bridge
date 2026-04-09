import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers.texts import txt_router
from handlers.callbacks import call_router


async def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(txt_router, call_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('start bot')
    asyncio.run(main())
