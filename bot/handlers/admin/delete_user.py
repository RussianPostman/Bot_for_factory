from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker

from bot.db import get_list_users, delete_user
from bot.handlers.keyboards.admin_kb import generate_users_board, UserCD
from bot.handlers.keyboards.admin_kb import ADMIN_MENU_BOARD


class DeleteUserStates(StatesGroup):
    """
        Состояния для категорий
    """
    waiting_for_id = State()


async def start_user_delete(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):

    await state.set_state(DeleteUserStates.waiting_for_id)
    users = await get_list_users(session_maker)
    await message.answer(
        'Выберите пользователя для удаления',
        reply_markup=generate_users_board(users)
        )


async def user_delete(
        query: types.CallbackQuery,
        callback_data: UserCD,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await state.clear()
    await delete_user(
        user_id=int(callback_data.user_id),
        session_maker=session_maker
        )
    # await delete_worksheet(int(callback_data.user_id))
    await SendMessage(
        text=f'Пользователь {callback_data.name} удалён',
        chat_id=query.from_user.id,
        reply_markup=ADMIN_MENU_BOARD
        )
