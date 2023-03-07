from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from bot.handlers.keyboards.admin_kb import UserCD
from bot.handlers.commands import start, help
from bot.handlers.admin.create_user import censel_hendler, start_user_create, \
    UserStates, waiting_for_id, waiting_for_name, user_create
from bot.handlers.admin.delete_user import start_user_delete, user_delete, \
    DeleteUserStates
from bot.handlers.admin.synchronization import start_synchronization, \
    SynchronizationStates, synchronization_roles, synchronization_products


__all__ = ['register_user_commands']


def register_user_commands(router: Router) -> Router:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())
    router.message.register(help, Command(commands=['help']))

    # хендлеры выхода из машины состояний
    router.message.register(censel_hendler, Command('cancel'), any_state)
    router.message.register(censel_hendler, F.text.casefold() == 'отмена' or 'Отмена', any_state)
    router.callback_query.register(censel_hendler, F.data == 'cancel', any_state)

    # создание пользователя
    router.message.register(start_user_create, F.text == 'Добавить пользователя')
    router.message.register(waiting_for_name, UserStates.waiting_for_name)
    router.message.register(waiting_for_id, UserStates.waiting_for_id)
    router.callback_query.register(user_create, UserStates.select_role, F.data == 'admin')
    router.callback_query.register(user_create, UserStates.select_role, F.data == 'worker')

    # удаление пользователя
    router.message.register(start_user_delete, F.text == 'Удалить Пользователя')
    router.callback_query.register(
        user_delete, DeleteUserStates.waiting_for_id, UserCD.filter(F.flag == '1')
        )

    # хендлеры синхронизации бд
    router.message.register(start_synchronization, F.text == 'Синхронизация')
    router.callback_query.register(
        synchronization_roles, SynchronizationStates.chose, F.data == 'synchronization_roles'
        )
    router.callback_query.register(
        synchronization_products, SynchronizationStates.chose, F.data == 'synchronization_products')

    # router.callback_query.register(start_category_create, F.data == 'start_category_create')
    # router.message.register(category_create, CategoryStates.waiting_for_name)

    # router.callback_query.register(RegisterCheck)
    # router.message.register(RegisterCheck)
