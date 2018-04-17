import json, csv
import simplekml
import numpy as np

kml = simplekml.Kml()
lses = []

path = r"G:\data\geography\test\N02-16_GML\N02-16_Station.geojson"
with open(path, 'r', encoding='utf8') as f:
    data = f.read()
data = json.loads(data)
for x in data["features"]:
    if x['properties']['運営会社'] == '京王電鉄':
        sta = x["geometry"]["coordinates"]
        sta_name = x["properties"]["駅名"]
        kml.newlinestring(name=sta_name, coords=sta)

        sta2 = np.mean(sta, axis=0).tolist()
        p = kml.newpoint(name=sta_name)
        p.coords = [(sta2[0], sta2[1])]

        lses.append([sta_name, sta2[0], sta2[1]])

kml.save("keio.kml")
print(lses)
with open("keio.csv", 'w') as f:
    ff = csv.writer(f, lineterminator='\n')
    ff.writerows(lses)