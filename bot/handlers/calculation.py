from datetime import datetime
from datetime import date, timedelta
import pandas


def sum_today(all_records: list[list[str]]):
    today = datetime.today().strftime('%Y-%m-%d')
    data = []
    count = 0
    for record in all_records:
        record: list
        if record[2] == today:
            data.append(record)
    for one_record in data:
        count += float(one_record[-2].replace(',', '.'))
    return count


def sum_month(all_records: list[list[str]]):
    data = []
    count = 0

    today = datetime.today().strftime('%Y-%m-%d')
    today = today.split('-')
    today = (int(today[0]), int(today[1]), int(today[2]))

    if today[2] == 10:
        return sum_today(all_records)
    elif today[2] > 10:
        sdate = date(today[0], today[1], 10)
    elif today[2] < 10:
        if today[1] == 1:
            sdate = date(today[0] - 1, 12, 10)
        else:
            sdate = date(today[0], today[1] - 1, 10)

    edate = date.today()
    result = pandas.date_range(
        sdate,
        edate,
        freq='d'
        ).strftime('%Y-%m-%d').tolist()

    for record in all_records:
        record: list
        if record[2] in result:
            data.append(record)
    for one_record in data:
        count += float(one_record[-2].replace(',', '.'))
    return count
