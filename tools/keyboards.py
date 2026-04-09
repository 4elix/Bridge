from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb_finish_register = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='success_first_name'),
            InlineKeyboardButton(text='Нет', callback_data='failed_first_name')
        ]
    ]
)


def kb_start_menu(role):
    func = ['Часто задаваемые вопрос', 'Написать менеджеру']
    if role == 'client':
        btn = [[KeyboardButton(text=b)] for b in func]
    elif role == 'admin':
        func.append('Работа с вопросами')
        btn = [[KeyboardButton(text=b)] for b in func]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return markup
