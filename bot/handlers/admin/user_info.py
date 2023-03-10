from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker

from bot.db import get_list_users
from bot.googlr_sheets.user_tools import read_reports
from bot.handlers.keyboards.admin_kb import generate_users_board, UserCD
from bot.handlers.keyboards.admin_kb import ADMIN_MENU_BOARD
from bot.handlers.calculation import sum_month


class UserInfoStates(StatesGroup):
    """
        Состояния для категорий
    """
    waiting_for_id = State()


async def start_user_info(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):

    await state.set_state(UserInfoStates.waiting_for_id)
    users = await get_list_users(session_maker)
    await message.answer(
        'Выберите пользователя',
        reply_markup=generate_users_board(users)
        )


async def user_info_month(
        query: types.CallbackQuery,
        callback_data: UserCD,
        state: FSMContext,
        ):
    await SendMessage(
        text='Считаем...',
        chat_id=query.from_user.id,
        )
    await state.clear()
    all_records = await read_reports(callback_data.user_id)
    month_sum = sum_month(all_records)
    await SendMessage(
        text=(f'С 10го числа пользователь {callback_data.name} '
              + f'заработал {month_sum}'),
        chat_id=query.from_user.id,
        reply_markup=ADMIN_MENU_BOARD
        )
