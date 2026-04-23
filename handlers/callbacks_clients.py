from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from tools.states import RegisterUser
from tools.keyboards import kb_start_menu, kb_pagination
from database.crud import work_user, work_faq

call_clients_router = Router()


@call_clients_router.callback_query(F.data.endswith('_first_name'))
async def react_btn_first_name(callback: CallbackQuery, state: FSMContext):
    variant = callback.data.split('_')[0]
    if variant == 'success':
        data = await state.get_data()
        role = 'admin' if 'admin001' in data['first_name'] else 'client'
        tg_id = callback.message.chat.id
        await work_user(data['first_name'], role, tg_id, part='create')
        await callback.message.answer(txt_start_fin, reply_markup=kb_start_menu(role))
        await state.clear()
    elif variant == 'failed':
        await state.set_state(RegisterUser.first_name)
        await callback.message.answer('Хорошо, введите ещё раз имя')


@call_clients_router.callback_query(F.data.startswith('page:'))
async def react_btn_paginate(callback: CallbackQuery):
    page = int(callback.data.split(':')[1])
    data = await work_faq(part='get')
    count_object = len(data)

    text = f'Вопрос: {data[page][1]}\nОтвет: {data[page][2]}\n\n\tСтраница: {page + 1}'
    await callback.message.edit_text(
        text, reply_markup=kb_pagination(page, count_object)
    )


@call_clients_router.callback_query(F.data == 'back_to_menu')
async def react_btn_btm(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    tg_id = callback.message.chat.id
    role = await work_user(tg_id, part='get')
    await callback.message.delete()
    await callback.message.answer('Хорошо, вот меню', reply_markup=kb_start_menu(role[2]))


