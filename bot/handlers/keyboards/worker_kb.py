"""
    Клавиатура для отображения постов
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.db import Category, Product, User


class CategoryCD(CallbackData, prefix='category_name'):
    """
        Обработка отрисовки списка категорий продуктов
    """
    flag: str = '1'
    category_name: str = None


class ProductCD(CallbackData, prefix='prod'):
    """
        Обработка отрисовки списка юзеров
    """
    flag: str = '1'
    name: str


class UserRoleCD(CallbackData, prefix='report_role'):
    """
        Обработка отрисовки списка ролей юзера
    """
    flag: str = '1'
    name: str


class SalarysCD(CallbackData, prefix='salarys'):
    """
        Обработка отрисовки списка почасовых ставок
    """
    flag: str = '1'
    salary: str = None


START_WORKER_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить отчёт о работе')
        ],
        [
            KeyboardButton(text='Узнать сумму в этом месяце'),
            KeyboardButton(text='Узнать cумму на сегоденя')
        ],
    ],
    resize_keyboard=True
)


SELECT_TYPE_REPORT = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сдельная'),
            KeyboardButton(text='Почасовая')
        ],
    ],
    resize_keyboard=True
)


def simple_generate_board(list_dt: list[str]) -> InlineKeyboardMarkup:
    """
    Простой генератор клавиатуры по списку
    list_dt: список ролей
    """

    builder = InlineKeyboardBuilder()
    for dt in list_dt:
        builder.button(
            text=dt,
            callback_data=SalarysCD(salary=dt).pack()
            )
    builder.button(text='Отмена', callback_data='cancel')
    builder.adjust(1)

    return builder.as_markup()


def generate_categorys_board(categorys: list[Category.name]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с категориями
    :categorys: список категорий для отображения
    """

    builder = InlineKeyboardBuilder()
    for category in categorys:
        builder.button(
            text=category,
            callback_data=CategoryCD(category_name=category).pack()
            )
    builder.button(text='Отмена', callback_data='cancel')
    builder.adjust(1)

    return builder.as_markup()


def generate_product_board(products: list[Product]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с продукцией категории
    :products: список наименований продукции для отображения
    """

    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(
            text=product.name,
            callback_data=ProductCD(
                name=product.name,
                ).pack()
            )
    builder.button(text='Отмена', callback_data='cancel')
    builder.adjust(1)

    return builder.as_markup()


def generate_roles_board(roles: list[User]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с ролями пользователя
    :products: список ролей
    """

    builder = InlineKeyboardBuilder()
    for role in roles:
        builder.button(
            text=role,
            callback_data=UserRoleCD(
                name=role,
                ).pack()
            )
    builder.button(text='Отмена', callback_data='cancel')
    builder.adjust(1)

    return builder.as_markup()
