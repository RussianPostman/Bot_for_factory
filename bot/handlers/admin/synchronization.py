"""Хендлеры синхронизирующие базу данных с гугл таблицей"""
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker

from bot.googlr_sheets.products_tools import read_category, read_products
from bot.googlr_sheets.user_tools import read_roles
from bot.db import create_role, get_roles_list, get_сategory_list, \
    create_category, get_products_names_list, update_product, create_product
from bot.handlers.keyboards.admin_kb import SYNCHRONIZATION_BOARD, \
    ADMIN_MENU_BOARD


class SynchronizationStates(StatesGroup):
    """
        Синхронизации баз данных
    """
    chose = State()


async def start_synchronization(message: types.Message, state: FSMContext):
    """
    Вход в состояние синхронизации
    """
    await state.set_state(SynchronizationStates.chose)
    await message.answer(
        'Что хотите синхронизировать?',
        reply_markup=SYNCHRONIZATION_BOARD)


async def synchronization_roles(
        query: types.CallbackQuery,
        session_maker: sessionmaker,
        state: FSMContext):
    """
    Синхронизует пользовательские роли
    """
    await state.clear()
    await SendMessage(
        text='Получаем список из гугл таблиц',
        chat_id=query.from_user.id)

    roles_list = await read_roles()
    db_roles_list = await get_roles_list(session_maker)
    for role_name in roles_list:
        if role_name not in db_roles_list:
            await SendMessage(
                text=f'Добавляем роль {role_name}',
                chat_id=query.from_user.id)
            await create_role(role_name, session_maker)
    await SendMessage(
        text='Роли синхронезированы',
        chat_id=query.from_user.id,
        reply_markup=ADMIN_MENU_BOARD)


async def synchronization_products(
        query: types.CallbackQuery,
        session_maker: sessionmaker,
        state: FSMContext):
    """
    Синхронизует детали и категории деталей
    """
    await state.clear()
    await SendMessage(
        text='Получаем продукты из гугл таблиц',
        chat_id=query.from_user.id)

    # синхроизация категорий
    category_list = await read_category()
    db_category_list_list = await get_сategory_list(session_maker)
    for category_name in category_list:
        if category_name not in db_category_list_list:
            await SendMessage(
                text=f'Добавляем категорию {category_name}',
                chat_id=query.from_user.id)
            await create_category(category_name, session_maker)
    await SendMessage(
        text='Категории синхронезированы',
        chat_id=query.from_user.id,
        reply_markup=ADMIN_MENU_BOARD)

    # синхроизация продуктов
    for cat in category_list:
        products_list = await read_products(cat)
        db_products_list = await get_products_names_list(session_maker, cat)

        for product in products_list:
            if product[0] not in db_products_list:
                await SendMessage(
                    text=f'Добавляем деталь {product[0]} в категорию {cat}',
                    chat_id=query.from_user.id)
                await create_product(product, cat, session_maker)
            else:
                await SendMessage(
                    text=f'Обновляем деталь {product[0]} в категории {cat}',
                    chat_id=query.from_user.id)
                await update_product(product, cat, session_maker)
    await SendMessage(
        text='Все детали синхронизированы',
        chat_id=query.from_user.id,
        reply_markup=ADMIN_MENU_BOARD)
