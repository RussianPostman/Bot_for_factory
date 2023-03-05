from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError

from bot.googlr_sheets.tools import read_roles
from bot.db import create_role, get_roles_list
from bot.handlers.keyboards.admin_kb import SYNCHRONIZATION_BOARD


class SynchronizationStates(StatesGroup):
    """
        Синхронизации баз данных
    """
    chose = State()


async def start_synchronization(message: types.Message, state: FSMContext):
    await state.set_state(SynchronizationStates.chose)
    await message.answer(
        'Что хотите синхронизировать?',
        reply_markup=SYNCHRONIZATION_BOARD)


async def synchronization_roles(
        query: types.CallbackQuery,
        session_maker: sessionmaker,
        state: FSMContext):
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
        chat_id=query.from_user.id)
