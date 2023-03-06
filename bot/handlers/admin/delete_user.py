from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker

from bot.db import get_list_users, delete_user
from bot.handlers.keyboards.admin_kb import generate_users_board, UserCD
from bot.googlr_sheets.tools import delete_worksheet


class DeleteUserStates(StatesGroup):
    """
        Состояния для категорий
    """
    waiting_for_id = State()


async def start_user_delete(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    await state.set_state(DeleteUserStates.waiting_for_id)
    users = await get_list_users(session_maker)
    await message.answer(
        'Выберите пользователя для удаления', reply_markup=generate_users_board(users))


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
    await delete_worksheet(int(callback_data.user_id))
    await SendMessage(
        text=f'Пользователь {callback_data.name} удалён',
        chat_id=query.from_user.id
        )


# async def waiting_for_name(message: types.Message, state: FSMContext):
#     await state.update_data(waiting_for_name=message.text)
#     await state.set_state(UserStates.waiting_for_id)
#     await message.answer('Введите Telegram id пользователя')


# async def waiting_for_id(message: types.Message, state: FSMContext):
#     await state.update_data(waiting_for_id=message.text)
#     await state.set_state(UserStates.select_role)
#     await message.answer('Выберите роли пользователя')
#     await SendMessage(
#         text='Админ имеет полный доступ к функциям бота, в том числе отправке отчётов о работе',
#         chat_id=message.from_user.id,
#         reply_markup=ADMIN_USER_ROLE)
#     await SendMessage(
#         text='Рабочий может только отправлять отчёты о работе',
#         chat_id=message.from_user.id,
#         reply_markup=WORKER_USER_ROLE)


# async def user_create(query: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
#     data = await state.get_data()
#     name = data['waiting_for_name']
#     user_id = int(data['waiting_for_id'])
#     await create_user_admin(user_id, name, session_maker)
#     await state.clear()
#     await SendMessage(
#         text=f'Пользователь {name} добавлен',
#         chat_id=query.from_user.id)
