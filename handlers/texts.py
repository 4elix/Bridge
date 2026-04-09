from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from tools.states import RegisterUser
from database.crud import work_user, work_faq
from tools.keyboards import kb_finish_register, kb_start_menu

txt_router = Router()


@txt_router.message(Command('start'))
async def react_cmd_start(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user_data = await work_user(tg_id, part='get')

    await state.clear()

    if user_data is None:
        await message.answer(txt_start_reg)
        await state.set_state(RegisterUser.first_name)
        return 0

    print(user_data)
    await message.answer(txt_start, reply_markup=kb_start_menu(user_data[2]))


@txt_router.message(RegisterUser.first_name)
async def get_first_name(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    text = f'Вас зовут: {first_name}. Если указано неверно, нажмите «Нет».'
    await message.answer(text, reply_markup=kb_finish_register)
