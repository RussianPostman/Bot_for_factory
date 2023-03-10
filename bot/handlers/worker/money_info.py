from aiogram.methods import SendMessage
from aiogram import types

from bot.googlr_sheets.user_tools import read_reports
from bot.handlers.keyboards.worker_kb import START_WORKER_BOARD
from bot.handlers.calculation import sum_month, sum_today


async def money_info_today(
        message: types.Message,
        ):
    await SendMessage(
        text='Считаем...',
        chat_id=message.from_user.id,
        )
    all_records = await read_reports(message.from_user.id)
    today_sum = sum_today(all_records)
    await SendMessage(
        text=f'Сегодня вы заработали {today_sum}',
        chat_id=message.from_user.id,
        reply_markup=START_WORKER_BOARD
        )


async def money_info_month(
        message: types.Message,
        ):
    await SendMessage(
        text='Считаем...',
        chat_id=message.from_user.id,
        )
    all_records = await read_reports(message.from_user.id)
    month_sum = sum_month(all_records)
    await SendMessage(
        text=f'С 10го числа вы заработали {month_sum}',
        chat_id=message.from_user.id,
        reply_markup=START_WORKER_BOARD
        )
