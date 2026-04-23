from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    first_name = State()


class CreateFaq(StatesGroup):
    question = State()
    answer = State()


class ChangeFaq(StatesGroup):
    faq_id = State()
    question = State()
    answer = State()