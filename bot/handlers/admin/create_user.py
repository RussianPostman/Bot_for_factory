from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError

from bot.db import create_user_admin, create_user_worker
from bot.handlers.keyboards.admin_kb import ADMIN_USER_ROLE, WORKER_USER_ROLE, \
    ADMIN_MENU_BOARD
from bot.googlr_sheets.user_tools import create_worksheet


REPORT_HEADS = [
    'ID', 'ФИО', 'Дата', 'Деталь', 'Количество', 'Цена',
    'Оклад', 'Комментарий', 'Сумма', 'Брак'
    ]


class UserStates(StatesGroup):
    """
        Состояния для категорий
    """
    waiting_for_name = State()
    waiting_for_id = State()
    select_role = State()


async def start_user_create(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.waiting_for_name)
    await message.answer('Введите имя нового пользователя')


async def waiting_for_name(message: types.Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await state.set_state(UserStates.waiting_for_id)
    await message.answer('Введите Telegram id пользователя')


async def waiting_for_id(message: types.Message, state: FSMContext):
    await state.update_data(waiting_for_id=message.text)
    await state.set_state(UserStates.select_role)
    await message.answer('Выберите роли пользователя')
    await SendMessage(
        text='Админ имеет полный доступ к функциям бота, в том числе отправке отчётов о работе',
        chat_id=message.from_user.id,
        reply_markup=ADMIN_USER_ROLE)
    await SendMessage(
        text='Рабочий может только отправлять отчёты о работе',
        chat_id=message.from_user.id,
        reply_markup=WORKER_USER_ROLE)


async def user_create(query: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    name = data['waiting_for_name']
    user_id = int(data['waiting_for_id'])
    if query.data == 'admin':
        await create_user_admin(user_id, name, session_maker)
        await create_worksheet(name=f'{name}_{user_id}', heads=REPORT_HEADS)
    elif query.data == 'worker':
        await create_user_worker(user_id, name, session_maker)
        await create_worksheet(name=f'{name}_{user_id}', heads=REPORT_HEADS)
    await state.clear()
    await SendMessage(
        text=f'Пользователь {name} добавлен',
        chat_id=query.from_user.id)


# функция выхода из машины состояний
async def censel_hendler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await SendMessage(
        text='Ок',
        chat_id=message.from_user.id,
        reply_markup=ADMIN_MENU_BOARD)
