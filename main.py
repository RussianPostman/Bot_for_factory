import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv

from bot.handlers import register_user_commands
from bot.settings import bot_commands

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TOKEN')

async def main():
    logging.basicConfig(level=logging.DEBUG)
    commands_for_bot = []

    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()
    bot = Bot(TELEGRAM_TOKEN)
    await bot.set_my_commands(commands=commands_for_bot)

    register_user_commands(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt,):
        print('Bot stoped')