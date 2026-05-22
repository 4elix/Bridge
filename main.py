import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers.commands import cmd_router
from handlers.texts_admin import txt_admin_router
from handlers.texts_clients import txt_client_router
from handlers.callbacks_admin import call_admin_router
from handlers.callbacks_clients import call_clients_router


async def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(
        cmd_router, txt_admin_router,
        txt_client_router, call_admin_router, call_clients_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('start bot')
    asyncio.run(main())
