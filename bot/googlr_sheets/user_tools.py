import asyncio
import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClientManager, \
    AsyncioGspreadSpreadsheet, AsyncioGspreadWorksheet

from google.oauth2.service_account import Credentials

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


# async def example(agcm):
#     agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
#     ss = await agc.open_by_url(USERS_SHEETS)
#     zero_ws = await ss.worksheet('My Test Worksheet')
#     pprint(await zero_ws.get_all_values())
#     print("All done!")


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
    await ss.add_worksheet(name, rows, cols)
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
