from aiogram import types
# from aiogram.types import Message


async def start(message: types.Message):
    """
    Хендлер для команды /start
    :param message:
    """
    return await message.answer('Started')


async def help(message: types.Message):
    """
    Хендлер для команды /help
    :param message:
    """
    return await message.answer('Help text')
