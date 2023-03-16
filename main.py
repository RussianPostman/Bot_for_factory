import os
import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv
from sqlalchemy import URL
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers import register_user_commands
from bot.settings import bot_commands
from bot.db import create_async_engine, get_session_maker
from bot.middleweres import RegisterCheck
from bot.handlers.apscheduler import salary_apdate

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

    postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username=os.getenv("POSTGRES_USER"),
        host='127.0.0.1',
        database=os.getenv("POSTGRES_DB"),
        port=8765,
        password=os.getenv("POSTGRES_PASSWORD")
    )

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    register_user_commands(dp)

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    apscheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    apscheduler.add_job(
        salary_apdate,
        "interval",
        hours=24,
        kwargs={'session_maker': session_maker}
        )

    apscheduler.start()
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt,):
        print('Bot stoped')
