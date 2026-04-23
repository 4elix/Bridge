from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tools.ghostwriter import *
from tools.states import CreateFaq, ChangeFaq
from database.crud import work_user, work_faq
from tools.keyboards import kb_create_faq, kb_save_faq, kb_work_faq, kb_change_faq

txt_admin_router = Router()


@txt_admin_router.message(F.text == 'Создать вопрос')
async def react_btn_r_create_faq(message: Message):
    tg_id = message.chat.id
    role = await work_user(tg_id, part='get')
    if role[2] != 'admin':
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


@txt_admin_router.message(F.text == 'Работать с вопросом')
async def react_btn_work_faq(message: Message):
    data = await work_faq(part='get')
    for faq_id, question, _ in data:
        await message.answer(f'Вопрос: {question}', reply_markup=kb_work_faq(faq_id))


@txt_admin_router.message(ChangeFaq.question)
async def get_question_for_change(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(ChangeFaq.answer)
    await message.answer(f'Введите измененный ответ на вопрос: {message.text}')


@txt_admin_router.message(ChangeFaq.answer)
async def get_answer_for_change(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    text = f'Id вопроса: {data["faq_id"]}\nВопрос: {data["question"]}\nОтвет на вопрос: {message.text}'
    await message.answer(text, reply_markup=kb_change_faq)
