import json, csv, sys
import simplekml
import numpy as np

class nazo:

    def __init__(self):
        self.path = r"G:\data\geography\test\N02-16_GML\N02-16_Station.geojson"
    
    def station(self, company="京王電鉄"):
        kml = simplekml.Kml()
        lses = []
        with open(self.path, 'r', encoding='utf8') as f:
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
        with open("stationdata\\{}.csv".format(company), 'w') as f:
            ff = csv.writer(f, lineterminator='\n')
            ff.writerows(lses)

if __name__ == '__main__':
    nazo = nazo()
    company = input(" > ")
    if company == '':
        company = '山万'
    nazo.station(company=company)
