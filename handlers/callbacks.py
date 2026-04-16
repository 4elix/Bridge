from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from database.crud import work_user, work_faq
from tools.states import RegisterUser, CreateFaq
from tools.keyboards import kb_start_menu, kb_create_faq

call_router = Router()


@call_router.callback_query(F.data.endswith('_first_name'))
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


@call_router.callback_query(F.data == 'back_to_menu')
async def react_btn_btm(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    tg_id = callback.message.chat.id
    role = await work_user(tg_id, part='get')[2]
    await callback.message.answer('Хорошо, вот меню', reply_markup=kb_start_menu(role))


@call_router.callback_query(F.data == 'create_faq')
async def react_btn_i_create_faq(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateFaq.question)
    await callback.message.answer('Введите название вопроса')


@call_router.callback_query(F.data.endswith('save_faq'))
async def react_btn_save_faq(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    if len(callback.data.split('_')) == 3:
        await state.clear()
        await callback.message.answer('Хорошо, выберите операцию', reply_markup=kb_create_faq)
    else:
        data = await state.get_data()

        await work_faq(data['question'], data['answer'], part='create')
        await callback.message.answer('Значения сохранены, выберите операцию', reply_markup=kb_create_faq)

