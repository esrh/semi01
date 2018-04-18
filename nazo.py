import json, csv, sys, time
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
        
    def choume(self, data, data2, cityname='千代田区'):#調べるデータ、町丁目座標データ、の順
        col = []
        for x in data2:
            if x[3] == cityname:
                col.append([x[5], x[6], x[7]])
        lses = []
        for i, x in enumerate(data):
            try:
                if x[1] == "":
                    xx = x[2]
                elif data[i+1][2] == "":
                    xx = x[1]
                else:
                    xx = ''
            except IndexError:
                xx = x[1]
            
            if xx != "":
                for ii in range(0,9):#0-8
                    xx = xx.replace(self.ntbl[0][ii], self.ntbl[1][ii])
                xx = xx.split('\n')[0]
                try:
                    n = [temp[0] for temp in col].index(xx)
                    nn = x[8]
                    if type(nn) != float:
                        nn = ''
                    ls = [xx, col[n][2], col[n][1], nn]
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
        ftbl = nazo.rcsv("ファイルテーブル.csv", encoding='sjis')#sjis,ヘッダなし
        data2 = nazo.rcsv(r"G:\data\geography\test\13_2006.csv", encoding='sjis')
        data4 = []
        for x in ftbl:
            path = r"G:\data\geography\test\商業統計\東京都小売" + '\\' + x[0]
            data = nazo.xls2csv(path=path)
            data3 = nazo.choume(data, data2, cityname=x[1])
            nazo.wcsv('temp\\{}.csv'.format(x[1]), data3)
            data4 = data4 + data3
        nazo.wcsv('temp\\temp3.csv', data4)
        
