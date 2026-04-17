from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from tools.states import RegisterUser
from database.crud import work_user, work_faq
from tools.keyboards import kb_finish_register, kb_pagination

txt_client_router = Router()


@txt_client_router.message(RegisterUser.first_name)
async def get_first_name(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    text = f'Вас зовут: {first_name}. Если указано неверно, нажмите «Нет».'
    await message.answer(text, reply_markup=kb_finish_register)


@txt_client_router.message(F.text == 'Часто задаваемые вопросы')
async def react_btn_show_faq(message: Message):
    data = await work_faq(part='get')
    page = 0
    count_object = len(data)
    await message.answer(f'Общей кол-во вопрос: {count_object}\n', reply_markup=ReplyKeyboardRemove())
    text = f'Вопрос: {data[0][1]}\nОтвет: {data[0][2]}\n\n\tСтраница: {page+1}'
    await message.answer(text, reply_markup=kb_pagination(page, count_object))


