from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tools.ghostwriter import *
from tools.states import RegisterUser, CreateFaq
from database.crud import work_user, work_faq
from tools.keyboards import kb_finish_register, kb_start_menu, kb_create_faq, kb_save_faq

txt_router = Router()


# ======================== Start / Register ===================
@txt_router.message(Command('start'))
async def react_cmd_start(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user_data = await work_user(tg_id, part='get')

    await state.clear()

    if user_data is None:
        await message.answer(txt_start_reg, reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterUser.first_name)
        return 0

    await message.answer(txt_start, reply_markup=kb_start_menu(user_data[2]))


@txt_router.message(RegisterUser.first_name)
async def get_first_name(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    text = f'Вас зовут: {first_name}. Если указано неверно, нажмите «Нет».'
    await message.answer(text, reply_markup=kb_finish_register)

# ======================== End Register ===================================


# ======================== Start Create Faq ===============================
@txt_router.message(F.text == 'Создать вопрос')
async def react_btn_r_create_faq(message: Message):
    tg_id = message.chat.id
    user_data = await work_user(tg_id, part='get')
    role = user_data[2]
    if role != 'admin':
        await message.answer(error_message, reply_markup=ReplyKeyboardRemove())
        return 0

    await message.answer('Выберите операцию', reply_markup=kb_create_faq)


@txt_router.message(CreateFaq.question)
async def get_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(CreateFaq.answer)

    await message.answer(f'Введите ответ на вопрос: {message.text}')


@txt_router.message(CreateFaq.answer)
async def get_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    question = await state.get_data()
    question = question['question']
    text = f'Вопрос: {question}\n\nОтвет на вопрос: {message.text}'
    await message.answer(text, reply_markup=kb_save_faq)
