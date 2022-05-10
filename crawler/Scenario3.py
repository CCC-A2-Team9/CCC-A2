# team:   group 9
# member:
# Zhaoxiang NING, 1261076, Luoyang, China
# Xinyi ZHOU, 1281911, Wuxi, China
# Haochu WANG, 1281962, Nantong, China
# Gengchang XU, 1214774, Zhuhai, China
# Shiming ZHENG, 1149897, Melbourne, Australia

import json
import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

file=shapefile.Reader('SA2_2016_AUST.shp')
shapes=file.shapes()
records=file.records()

# Collect boundary of the suburbs
suburbId = [692, 694, 695, 696, 698, 699, 700, 701, 703, 707, 714]
suburbName = ["Flemington", "Carlton", "Docklands", "East Melbourne", "Kensington", "Melbourne", "North Melbourne", "Parkville", "Southbank", "Port Melbourne", "South Yarra - East"]
sub_plon = []
for i in range(len(shapes)):
    # Using the points information to draw the ploygon
    if i in suburbId:
        polygon = Polygon(shapes[i].points)
        sub_plon.append(polygon)
sub_info = list(zip(suburbName,sub_plon))


with open("twitter-melb.json", "rb") as f:
    counter = 0
    total_line = 2500002
    dic = {}
    for line in f:
        if 0 < counter < total_line-2:
            tweet = json.loads(line[0:len(line) - 3])
            content = tweet['doc']['text']
            id = tweet['doc']['_id']
            coord = tweet['doc']['coordinates']
            if(coord):
                coordinate = tweet['doc']['coordinates']['coordinates']
            else:
                counter += 1
                continue
            lan = tweet['doc']['user']['lang']
            point = Point(coordinate[0],coordinate[1])
            for sub in sub_info:
                # Return true if the point is in the ploygon
                if sub[1].contains(point):
                    # Collect the result
                    dic[id] = [sub[0], lan]

        if counter == total_line-2:
            tweet = json.loads(line[0:len(line) - 2])
            content = tweet['doc']['text']
            id = tweet['doc']['_id']
            coord = tweet['doc']['coordinates']
            if(coord):
                coordinate = tweet['doc']['coordinates']['coordinates']
            else:
                counter += 1
                continue
            lan = tweet['doc']['user']['lang']
            point = Point(coordinate[0],coordinate[1])
            for sub in sub_info:
                # Return true if the point is in the ploygon
                if sub[1].contains(point):
                    # Collect the result
                    dic[id] = [sub[0], lan]
        counter += 1
    print(counter)

#convert dic to json file
dict_json=json.dumps(dic)
with open('file.json','w+') as file:
    file.write(dict_json)
