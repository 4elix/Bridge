from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from tools.states import RegisterUser
from tools.keyboards import kb_start_menu
from database.crud import work_user, work_faq

call_router = Router()


@call_router.callback_query(F.data.endswith('_first_name'))
async def react_btn_first_name(callback: CallbackQuery, state: FSMContext):
    variant = callback.data.split('_')[0]
    if variant == 'success':
        data = await state.get_data()
        role = 'admin' if data['first_name'] in 'admin001' else 'client'
        tg_id = callback.message.chat.id
        await work_user(data['first_name'], role, tg_id, part='create')
        await callback.message.answer(txt_start_fin, reply_markup=kb_start_menu(role))
        await state.clear()
    elif variant == 'failed':
        await state.set_state(RegisterUser.first_name)
        await callback.message.answer('Хорошо, введите ещё раз имя')
