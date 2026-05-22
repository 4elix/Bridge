from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tools.ghostwriter import *
from database.crud import work_user
from tools.states import RegisterUser
from tools.keyboards import kb_start_menu

cmd_router = Router()


@cmd_router.message(Command('start'))
async def react_cmd_start(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user_data = await work_user(tg_id, part='get')

    await state.clear()

    if user_data is None:
        await message.answer(txt_start_reg, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterUser.first_name)
        return 0

    await message.answer(txt_start, reply_markup=kb_start_menu(user_data[2]))

