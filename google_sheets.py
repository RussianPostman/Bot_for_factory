import time

import gspread


class GoogleTable:
    def __init__(self, json_way , url):
        self.json_way = json_way
        self.url = url
        self.x = 0
        self.y = 1

    def authorisation(self):
        gc = gspread.service_account(self.json_way)
        sh = gc.open_by_url(self.url)
        try:
            return sh
        except:
            time.sleep(1)

    def set_list(self, x):
        self.x = x

    def find_all_data(self,data):
        wks = self.authorisation().get_worksheet(self.x)
        return wks.findall(data)

    def find_data(self,data):
        wks = self.authorisation().get_worksheet(self.x)
        return wks.find(data)

    def delete_data(self, data):
        wks = self.authorisation().get_worksheet(self.x)
        if type(data) == type([]):
            for i in data:
                try:
                    wks.update(str(wks.find(i)).split(" ")[1], "")
                except:
                    time.sleep(60)
                    wks.update(str(wks.find(i)).split(" ")[1], "")
        elif type(data) == type(""):
            try:
                wks.update(str(wks.find(data)).split(" ")[1], "")
            except:
                time.sleep(60)
                wks.update(str(wks.find(data)).split(" ")[1], "")
        else:
            return 0

    def total_str(self):
        wks = self.authorisation().get_worksheet(self.x)
        data = self.read_data()
        while True:
            if self.y < len(data):
                self.y += 10
            elif self.y > len(data):
                self.y -= 1
            elif self.y == len(data):
                return True
            else:
                return False

    def load_data(self, data):
        wks = self.authorisation().get_worksheet(self.x)
        abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.total_str() :
            self.y += 1
            print(self.y)
            for i in range(len(data)):
                time.sleep(0.2)
                print(f"{abc[i]}{self.y}", data[i])
                wks.update(f"{abc[i]}{self.y}", data[i])

    def read_data(self):
        wks = self.authorisation().get_worksheet(self.x)
        return wks.get_all_values()

    def read_str(self, row):
        wks = self.authorisation().get_worksheet(self.x)
        return wks.row_values(row)

    def read_col(self,col):
        wks = self.authorisation().get_worksheet(self.x)
        return wks.col_values(col)

    def read_avto(self):
        data = []
        try:
            for i in range(len(self.get_title())):
                self.set_list(i)
                wks = self.authorisation().get_worksheet(self.x)
                data1 = wks.get_all_values()
                data.append(data1)
            return data
        except:
            time.sleep(60)
            for i in range(len(self.get_title())):
                self.set_list(i)
                wks = self.authorisation().get_worksheet(self.x)
                data1 = wks.get_all_values()
                data.append(data1)
            return data

    def get_title(self):
        sh = self.authorisation()
        return sh.worksheets()



