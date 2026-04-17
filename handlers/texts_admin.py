from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from tools.states import CreateFaq
from database.crud import work_user, work_faq
from tools.keyboards import kb_create_faq, kb_save_faq

txt_admin_router = Router()

@txt_admin_router.message(F.text == 'Создать вопрос')
async def react_btn_r_create_faq(message: Message):
    tg_id = message.chat.id
    user_data = await work_user(tg_id, part='get')
    role = user_data[2]
    if role != 'admin':
        await message.answer(error_message, reply_markup=ReplyKeyboardRemove())
        return 0

    await message.answer('Выберите операцию', reply_markup=kb_create_faq)


@txt_admin_router.message(CreateFaq.question)
async def get_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(CreateFaq.answer)

    await message.answer(f'Введите ответ на вопрос: {message.text}')


@txt_admin_router.message(CreateFaq.answer)
async def get_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    question = await state.get_data()
    question = question['question']
    text = f'Вопрос: {question}\n\nОтвет на вопрос: {message.text}'
    await message.answer(text, reply_markup=kb_save_faq)

