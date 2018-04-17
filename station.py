import json, csv, sys
import simplekml
import numpy as np
import xlrd

class nazo:
    def __init__(self):
        self.testpath = 'G:\\data\\geography\\test\\'
        self.ntbl = []
        with open("漢数字テーブル.csv", mode='r') as f:
            x = f.read().split('\n')
        for xx in x:
            self.ntbl.append(xx.split(","))
        print(self.ntbl)
        
    def xls2csv(self, path):
        data = []
        book = xlrd.open_workbook(path)
        a = book.sheet_by_index(0)
        for row in range(a.nrows):
            aaa = []
            for col in range(a.ncols):
                aaa.append(a.cell(row, col).value)
            #print(aaa)
            data.append(aaa)
        with open("temp\\temp.csv", 'w', encoding='utf8') as f:
            ff = csv.writer(f, lineterminator='\n')
            ff.writerows(data)
        return data
        
    def choume(self, data, data2):
        col = [row[5] for row in data2]
        lses = []
        for i, x in enumerate(data):
            xx = x[2]
            if xx != "":
                for ii in range(0,9):#0-8
                    xx = xx.replace(self.ntbl[0][ii], self.ntbl[1][ii])
                xx = xx.split('\n')[0]
                n = col.index(xx)
                ls = [xx, data2[n][7], data2[n][6]]
            else:
                ls = []
            lses.append(ls)
        print(lses)
            
    def station(self, company="京王電鉄"):
        path = r"G:\data\geography\test\N02-16_GML\N02-16_Station.geojson"
        kml = simplekml.Kml()
        lses = []
        with open(path, 'r', encoding='utf8') as f:
            data = f.read()
        data = json.loads(data)
        for x in data["features"]:
            if x['properties']['運営会社'] == company:
                sta = x["geometry"]["coordinates"]
                sta_name = x["properties"]["駅名"]
                kml.newlinestring(name=sta_name, coords=sta)

                sta2 = np.mean(sta, axis=0).tolist()
                p = kml.newpoint(name=sta_name)
                p.coords = [(sta2[0], sta2[1])]

                lses.append([sta_name, sta2[0], sta2[1]])

        kml.save("stationdata\\{}.kml".format(company))
        print(lses)
        with open("stationdata\\{}.csv".format(company),encoding="utf8", mode='w') as f:
            ff = csv.writer(f, lineterminator='\n')
            ff.writerows(lses)

if __name__ == '__main__':
    nazo = nazo()
    i = int(input(""))
    if i == 1:
        company = input(" > ")
        if company == '':
            company = '山万'
        nazo.station(company=company)
    if i == 2:
        path = r'G:\data\geography\test\町丁目\多摩市\多摩市小売.xls'
        data = nazo.xls2csv(path=path)
        path = r'G:\data\geography\test\13224-10.0b\13224_2016.csv'
        data2 = []
        with open(path, 'r') as f:
            for row in csv.reader(f):
                data2.append(row)
        nazo.choume(data,data2)