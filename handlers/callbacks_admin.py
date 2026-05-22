from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tools.ghostwriter import *
from database.crud import work_faq, work_user
from tools.states import CreateFaq, ChangeFaq
from tools.keyboards import kb_create_faq, kb_start_menu

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


@call_admin_router.callback_query(F.data.startswith('delete_faq'))
async def react_btn_delete_faq(callback: CallbackQuery):
    _, _, faq_id = callback.data.split('_')
    await work_faq(faq_id, part='delete')
    await callback.message.answer('Вопрос удален')


@call_admin_router.callback_query(F.data.startswith('change_faq'))
async def react_btn_change_faq(callback: CallbackQuery, state: FSMContext):
    _, _, faq_id = callback.data.split('_')
    await state.update_data(faq_id=faq_id)
    await state.set_state(ChangeFaq.question)
    await callback.message.answer(f'Введите текст для изменения вопроса №{faq_id}')


@call_admin_router.callback_query(F.data.in_(['save_change_faq', 'dont_change_faq']))
async def react_btn_change(callback: CallbackQuery, state: FSMContext):
    role = await work_user(callback.message.chat.id, part='get')
    if 'dont' in callback.data.split('_'):
        await state.clear()
        await callback.message.answer('Хорошо, выберите операцию', reply_markup=kb_start_menu(role[2]))
    else:
        data = await state.get_data()
        await work_faq(data['question'], data['answer'], data['faq_id'], part='update')
        await callback.message.answer('Вопрос изменен', reply_markup=kb_start_menu(role[2]))
