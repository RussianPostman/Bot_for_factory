from aiogram import types
# from aiogram.types import Message

from sqlalchemy.orm import sessionmaker

from bot.handlers.keyboards.admin_kb import ADMIN_MENU_BOARD


async def start(message: types.Message):
    """
    Хендлер для команды /start
    :param message:
    """
    return await message.answer('Started', reply_markup=ADMIN_MENU_BOARD)


async def help(message: types.Message):
    """
    Хендлер для команды /help
    :param message:
    """
    return await message.answer('Help text')


# async def generate(message: types.Message, session_maker: sessionmaker):
#     """
#     Хендлер для команды /gen
#     :param message:
#     """
#     print('generate start')
#     await create_category(name='Kamaz', session_maker=session_maker)
#     print('generate finish')

#     return await message.answer('Kamaz')


# async def generate(message: types.Message, session_maker: sessionmaker):
#     """
#     Хендлер для команды /gen
#     :param message:
#     """
#     print('generate start')
#     await create_category(name='Kamaz', session_maker=session_maker)
#     print('generate finish')

#     return await message.answer('Kamaz')