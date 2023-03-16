from datetime import datetime

from sqlalchemy.orm import sessionmaker

from bot.db import list_without_admins, User
from bot.handlers.calculation import sum_month
from bot.googlr_sheets.user_tools import read_reports
from bot.googlr_sheets.user_tools import add_salary


async def salary_apdate(session_maker: sessionmaker):
    todey = datetime.today().strftime('%Y-%m-%d')
    todey_list = todey.split('-')
    if todey_list[2] == '9':
        users = await list_without_admins(session_maker)
        print(users)
        for user in users:
            user: User
            all_records = await read_reports(user.user_id)
            month_sum = sum_month(all_records)
            await add_salary(user, month_sum, todey)
