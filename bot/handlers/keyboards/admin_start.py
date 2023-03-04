"""
    Клавиатура для отображения постов
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ADMIN_MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить пользователя'),
            KeyboardButton(text='Удалить Пользователя'),
        ]
    ],
    resize_keyboard=True
)


# CATEGORY_ADD_BOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Добавить категорию', callback_data='start_category_create'),
#             # InlineKeyboardButton(text='Рекламировать', callback_data=PostCD(action=PostCDAction.PR).pack()),
#         ],
#     ]
# )
