"""
    Клавиатура для отображения постов
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.db.user import User
from bot.googlr_sheets.user_tools import USERS_SHEETS
from bot.googlr_sheets.products_tools import RPODUCTS_SHEETS


class UserCD(CallbackData, prefix='user_list'):
    """
        Обработка отрисовки списка юзеров
    """
    flag: str = '1'
    user_id: str = None
    name: str = None


ADMIN_MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить пользователя'),
            KeyboardButton(text='Удалить пользователя'),
        ],
        [
            KeyboardButton(text='Информация о пользователе'),
            KeyboardButton(text='Перейти к Google таблицам'),
        ],
        [
            KeyboardButton(text='Синхронизация')
        ]
    ],
    resize_keyboard=True
)


GOOGLE_SHEETS_LINK = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Таблицы пользователей', url=USERS_SHEETS)
        ],
        [
            InlineKeyboardButton(text='Таблицы деталей', url=RPODUCTS_SHEETS)
        ],
    ]
)


SYNCHRONIZATION_BOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Роли', callback_data='synchronization_roles')
        ],
        [
            InlineKeyboardButton(text='Детали', callback_data='synchronization_products')
        ],
    ]
)


ADMIN_USER_ROLE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Администратор', callback_data='admin')
        ]
    ]
)


WORKER_USER_ROLE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рабочий', callback_data='worker')
        ]
    ]
)


def generate_users_board(users: list[User]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с пользователями
    :param roles: список постов для отображения
    :return:
    """

    builder = InlineKeyboardBuilder()
    for user in users:
        builder.button(
            text=user.name,
            callback_data=UserCD(user_id=user.user_id, name=user.name).pack()
            )
    builder.button(text='Отмена', callback_data='cancel')
    builder.adjust(1)

    return builder.as_markup()
