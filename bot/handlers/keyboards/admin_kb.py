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
        ],
        [
            KeyboardButton(text='Синхронизация')
        ]
    ],
    resize_keyboard=True
)


SYNCHRONIZATION_BOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Роли', callback_data='synchronization_roles')
        ],
        [
            InlineKeyboardButton(text='Детали', callback_data='synchronization_products')
        ],
        [
            InlineKeyboardButton(text='Отчёты', callback_data='synchronization_reports')
        ]
    ]
)
