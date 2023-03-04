from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError

from bot.db import create_category


class CategoryStates(StatesGroup):
    """
        Состояния для категорий
    """
    waiting_for_name = State()


async def start_category_create(message: types.Message, state: FSMContext):
    await state.set_state(CategoryStates.waiting_for_name)
    await message.answer('Введите название новой категории')


async def category_create(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    name = message.text
    await state.clear()
    try:
        await create_category(name=name, session_maker=session_maker)
        
    except ProgrammingError:
        await message.answer('Ошибка. Возможно вы ввеи недопустимые символы')

# функция выхода из машины состояний
async def censel_hendler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Ok')
