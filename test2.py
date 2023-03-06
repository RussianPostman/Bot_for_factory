import asyncio
from pprint import pprint

import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClient, AsyncioGspreadSpreadsheet, AsyncioGspreadWorksheet

# from google-auth package
from google.oauth2.service_account import Credentials

MAIL_URL = 'https://docs.google.com/spreadsheets/d/1ANGDNWvPXYmmJE_UeVSHy6DaBONk2vBtEgkWG7_mHe4/edit#gid=0'


def get_creds():
    creds = Credentials.from_service_account_file("bot/docs/creds.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


async def example(agcm):
    agc: gspread_asyncio.AsyncioGspreadClient = await agcm.authorize()

    ss = await agc.open_by_url("https://docs.google.com/spreadsheets/d/1WykXiBfTg2bzMPvFvehFDbVHrT65WWYuJiZ8H3pE95A")

    # ws = await ss.add_worksheet("My Test Worksheet", 10, 5)
    zero_ws = await ss.worksheets() # worksheet('My Test Worksheet')
    print(zero_ws)
    zero_ws1 = await ss.get_title() # worksheet('My Test Worksheet')
    print(zero_ws1)
    for i in zero_ws:
        print(i.title)

    # Write some stuff to both spreadsheets.
    # for row in range(1, 11):
    #     for col in range(1, 6):
    #         val = "{0}/{1}".format(row, col)
    #         await ws.update_cell(row, col, val + " ws")
    #         await zero_ws.update_cell(row, col, val + " zero ws")
    # print("All done!")
    # for row in range(1, 11):
    #     await zero_ws.append_rows([['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3'], ['1', '2', '3'],])
    # pprint(await zero_ws.get_all_values())
    print("All done!")


async def get_ws_by_id(id: int) -> AsyncioGspreadWorksheet:
    agc: AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url("https://docs.google.com/spreadsheets/d/1ANGDNWvPXYmmJE_UeVSHy6DaBONk2vBtEgkWG7_mHe4")

    worksheets = await ss.worksheets()
    for ws in worksheets:
        ws: AsyncioGspreadWorksheet
        if ws.title.endswith(str(id)):
            print(ws.title)
            return ws
    print('Таблица не нашлась\n')


asyncio.run(get_ws_by_id(2125332262))
