from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from sqlalchemy.orm import sessionmaker

from bot.handlers.keyboards.admin_kb import ADMIN_MENU_BOARD
from bot.handlers.keyboards.worker_kb import START_WORKER_BOARD
from bot.db import is_user_admin


async def start(message: types.Message, session_maker: sessionmaker):
    """
    Хендлер для команды /start
    :param message:
    """
    if await is_user_admin(message.from_user.id, session_maker):
        return await message.answer(
            'Started', reply_markup=ADMIN_MENU_BOARD)
    else:
        return await message.answer(
            'Started', reply_markup=START_WORKER_BOARD)


async def help(message: types.Message, session_maker: sessionmaker):
    """
    Хендлер для команды /help
    :param message:
    """
    # return await message.answer(
    #         'Started', reply_markup=ADMIN_MENU_BOARD)
    if is_user_admin(message.from_user.id, session_maker):
        return await message.answer(
            'Started', reply_markup=ADMIN_MENU_BOARD)
    else:
        return await message.answer(
            'Started', reply_markup=START_WORKER_BOARD)


# функция выхода из машины состояний
async def censel_hendler(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    if await is_user_admin(message.from_user.id, session_maker):
        return await SendMessage(
            text='Дейстаия отменены',
            chat_id=message.from_user.id,
            reply_markup=ADMIN_MENU_BOARD)
    else:
        return await SendMessage(
            text='Дейстаия отменены',
            chat_id=message.from_user.id,
            reply_markup=START_WORKER_BOARD)
