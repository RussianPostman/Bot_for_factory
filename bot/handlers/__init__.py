from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from bot.handlers.commands import start, help
from bot.handlers.admin.create_user import censel_hendler
from bot.handlers.admin.synchronization import start_synchronization, \
    SynchronizationStates, synchronization_roles
from bot.handlers.admin.synchronization import SynchronizationStates


__all__ = ['register_user_commands']


def register_user_commands(router: Router) -> Router:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())
    router.message.register(help, Command(commands=['help']))

    router.message.register(censel_hendler, Command('cancel'), any_state)
    router.message.register(censel_hendler, F.text.casefold() == 'отмена' or 'Отмена', any_state)

    # хендлеры синхронизации бд
    router.message.register(start_synchronization, F.text == 'Синхронизация')
    router.callback_query.register(
        synchronization_roles,
        SynchronizationStates.chose,
        F.data == 'synchronization_roles'
        )

    # router.callback_query.register(start_category_create, F.data == 'start_category_create')
    # router.message.register(category_create, CategoryStates.waiting_for_name)

    # router.callback_query.register(RegisterCheck)
    # router.message.register(RegisterCheck)
