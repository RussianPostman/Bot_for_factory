import os
import asyncio
from pprint import pprint
import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClientManager, \
    AsyncioGspreadSpreadsheet, AsyncioGspreadWorksheet
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials

load_dotenv()

RPODUCTS_SHEETS = os.getenv('RPODUCTS_SHEETS')


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


async def read_category(agcm: AsyncioGspreadClientManager = agcm) -> list[str]:
    """
    Инструмент синхронизации. Выдаёт список категорий из гугл кадендаря
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(RPODUCTS_SHEETS)
    worksheets = await ss.worksheets()
    worksheet_list = []
    for ws in worksheets:
        worksheet_list.append(ws.title)
    return worksheet_list


async def read_products(name: str, agcm: AsyncioGspreadClientManager = agcm) -> list[list[str]]:
    """
    Инструмент синхронизации. Выдаёт список деталей по названию категории
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(RPODUCTS_SHEETS)
    worksheet = await ss.worksheet(name)
    list_values = await worksheet.get_all_values()
    list_values.pop(0)
    return list_values
