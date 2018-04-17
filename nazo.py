import json, csv, sys
import simplekml
import numpy as np
import xlrd

class nazo:
    def __init__(self):
        self.testpath = 'G:\\data\\geography\\test\\'
        self.ntbl = []
        #漢数字テーブルはSJISです
        with open("漢数字テーブル.csv", mode='r') as f:
            x = f.read().split('\n')
        for xx in x:
            self.ntbl.append(xx.split(","))
        print(self.ntbl)
        
    def wcsv(self, path, data, encoding='utf8'):
        with open(path, 'w', encoding=encoding) as f:
            ff = csv.writer(f, lineterminator='\n')
            ff.writerows(data)

    def rcsv(self, path, encoding='utf8'):
        data = []
        with open(path, 'r', encoding=encoding) as f:
            for row in csv.reader(f):
                data.append(row)
        return data
        
    
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
        
    def choume(self, data, data2):#調べるデータ、町丁目座標データ、の順
        col = [row[5] for row in data2]
        lses = []
        for i, x in enumerate(data):
            if x[1] == "":
                xx = x[2]
            elif data[i+1][2] == "":
                xx = x[1]
            else:
                xx = ''
            if xx != "":
                for ii in range(0,9):#0-8
                    xx = xx.replace(self.ntbl[0][ii], self.ntbl[1][ii])
                xx = xx.split('\n')[0]
                try:
                    n = col.index(xx)
                    nn = x[8]
                    if type(nn) != float:
                        nn = ''
                    ls = [xx, data2[n][7], data2[n][6], nn]
                except ValueError:
                    ls = []
            else:
                ls = []
            lses.append(ls)
        self.wcsv('temp\\temp2.csv', lses)
        return lses
        
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
        return lses

if __name__ == '__main__':
    nazo = nazo()
    i = int(input(""))
    if i == 1:
        company = input(" > ")
        if company == '':
            company = '山万'
        nazo.station(company=company)
    if i == 2:
        ftbl = nazo.rcsv("ファイルテーブル.csv")#utf8,ヘッダあり
        
        path = r'G:\data\geography\test\町丁目\多摩市\多摩市小売.xls'
        data = nazo.xls2csv(path=path)
        path = r'G:\data\geography\test\13224-10.0b\13224_2016.csv'
        data2 = nazo.rcsv(path, encording='sjis')
        data3 = nazo.choume(data,data2)
        print(data3)
