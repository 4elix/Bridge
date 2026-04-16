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
    if role == 'admin':
        func.append('Создать вопрос')

    btn = [[KeyboardButton(text=b)] for b in func]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return markup


kb_create_faq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать новый вопрос', callback_data='create_faq')],
    [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')]
])

kb_save_faq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить', callback_data='save_faq')],
    [InlineKeyboardButton(text='Не сохранять', callback_data='dont_save_faq')]
])
