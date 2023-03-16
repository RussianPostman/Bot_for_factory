import gspread
import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClientManager, \
    AsyncioGspreadSpreadsheet, AsyncioGspreadWorksheet
from asyncpg.exceptions import UniqueViolationError

from google.oauth2.service_account import Credentials

from bot.db import User

USERS_SHEETS = "https://docs.google.com/spreadsheets/d/1ANGDNWvPXYmmJE_UeVSHy6DaBONk2vBtEgkWG7_mHe4"


def get_creds():
    creds = Credentials.from_service_account_file("bot/docs/creds.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


async def get_ws_by_id(id: int, ss: AsyncioGspreadSpreadsheet) -> AsyncioGspreadWorksheet:
    worksheets = await ss.worksheets()
    for ws in worksheets:
        ws: AsyncioGspreadWorksheet
        if ws.title.endswith(str(id)):
            return ws
    print('Таблица не нашлась\n')


agcm = AsyncioGspreadClientManager(get_creds)


async def create_worksheet(
        name: str,
        heads: list[str],
        agcm: AsyncioGspreadClientManager = agcm,
        rows: int = 3,
        cols: int = 10
        ):
    """
    Создать гугл таблицу
    :name:
    :heads:
    :rows:
    :cols:
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    try:
        new_worksheet = await ss.worksheet(name)
    except StopIteration:
        await ss.add_worksheet(name, rows, cols)
        new_worksheet = await ss.worksheet(name)
    except gspread.exceptions.WorksheetNotFound:
        await ss.add_worksheet(name, rows, cols)
        new_worksheet = await ss.worksheet(name)
    except UniqueViolationError:
        new_worksheet = await ss.worksheet(name)
    await new_worksheet.append_row(heads)


async def delete_worksheet(
        user_id: int,
        ):
    """
    Удаляет таблицу юзера пл его ТГ id
    :user_id:
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    worksheet: AsyncioGspreadWorksheet = await get_ws_by_id(user_id, ss)
    await ss.del_worksheet(worksheet)
    print('Таблица удалена')


async def read_roles(agcm: AsyncioGspreadClientManager = agcm):
    """
    Инструмент синхронизации. Выдаёт список ролей из гугл кадендаря
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    role_ws = await ss.worksheet('Роли')
    return await role_ws.col_values(1)


async def read_salarys(agcm: AsyncioGspreadClientManager = agcm):
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    role_ws = await ss.worksheet('Оклады')
    return await role_ws.col_values(1)


async def read_reports(
        user_id: str = 'Ежемесячные отчёты',
        agcm: AsyncioGspreadClientManager = agcm
        ):
    """
    Считывает все отчёты чтобы расчитать итоговый заработок
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    worksheet = await get_ws_by_id(user_id, ss)
    list_values = await worksheet.get_all_values()
    list_values.pop(0)
    return list_values


async def add_reports(
        values: dict,
        user_id: str = 'Ежемесячные отчёты',
        agcm: AsyncioGspreadClientManager = agcm
        ):
    """
    Считывает все отчёты чтобы расчитать итоговый заработок
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    data_list = []
    worksheet = await get_ws_by_id(user_id, ss)
    data_list.append(values.get('user_id'))
    data_list.append(values.get('username'))
    data_list.append(values.get('deta'))
    data_list.append(values.get('product'))
    data_list.append(values.get('count'))
    data_list.append(values.get('prise'))
    data_list.append(values.get('salary'))
    data_list.append(values.get('comment'))
    data_list.append(values.get('amount'))
    data_list.append(values.get('marriage'))

    await worksheet.append_row(data_list)


async def add_salary(
        user: User,
        salary: float,
        date: str,
        agcm: AsyncioGspreadClientManager = agcm
        ) -> None:
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    ws = await ss.worksheet('Ежемесячные отчёты')
    row = []
    row.append(user.user_id)
    row.append(user.name)
    row.append(date)
    row.append(salary)
    await ws.append_row(row)
