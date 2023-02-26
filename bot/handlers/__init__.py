from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandStart

from bot.handlers.commands import start, help

__all__ = ['register_user_commands']


def register_user_commands(router: Router) -> Router:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())
    router.message.register(help, Command(commands=['help']))
