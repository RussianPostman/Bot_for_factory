import asyncio
import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClientManager

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
        cols: int = 3
        ):
    """
    Создать гугл таблицу
    :param name:
    :param heads:
    :rows:
    :cols:
    """
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    await ss.add_worksheet(name, rows, cols)
    new_worksheet = await ss.worksheet(name)
    await new_worksheet.append_row(heads)


async def read_roles(agcm: AsyncioGspreadClientManager = agcm):
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(USERS_SHEETS)
    role_ws = await ss.worksheet('Роли')
    return await role_ws.col_values(1)
