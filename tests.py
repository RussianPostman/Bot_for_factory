import gspread
from pprint import pprint

from google_sheets import GoogleTable


def authorisation(json_way, url):
    gc = gspread.service_account(json_way)
    sh = gc.open_by_url(url)
    return sh


gc = gspread.service_account('docs/creds.json')


wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WykXiBfTg2bzMPvFvehFDbVHrT65WWYuJiZ8H3pE95A/edit#gid=0")


table = GoogleTable(
    json_way='docs/creds.json',
    url="https://docs.google.com/spreadsheets/d/1WykXiBfTg2bzMPvFvehFDbVHrT65WWYuJiZ8H3pE95A/edit#gid=0"
)

worksheet = wks.get_worksheet(0)

val = worksheet.cell(1, 2).value
cell = worksheet.acell('B3', value_render_option='FORMULA').value
values_list = worksheet.get_all_records()

pprint(values_list)
# print(cell)