from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    first_name = State()