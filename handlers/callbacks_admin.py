from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from tools.states import CreateFaq
from tools.keyboards import kb_create_faq
from database.crud import work_user, work_faq

call_admin_router = Router()


@call_admin_router.callback_query(F.data == 'create_faq')
async def react_btn_i_create_faq(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateFaq.question)
    await callback.message.answer('Введите название вопроса')


@call_admin_router.callback_query(F.data.endswith('save_faq'))
async def react_btn_save_faq(callback: CallbackQuery, state: FSMContext):
    if len(callback.data.split('_')) == 3:
        await state.clear()
        await callback.message.answer('Хорошо, выберите операцию', reply_markup=kb_create_faq)
    else:
        data = await state.get_data()

        await work_faq(data['question'], data['answer'], part='create')
        await callback.message.answer('Значения сохранены, выберите операцию', reply_markup=kb_create_faq)

