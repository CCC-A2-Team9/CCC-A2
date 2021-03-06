# team:   group 9
# member:
# Zhaoxiang NING, 1261076, Luoyang, China
# Xinyi ZHOU, 1281911, Wuxi, China
# Haochu WANG, 1281962, Nantong, China
# Gengchang XU, 1214774, Zhuhai, China
# Shiming ZHENG, 1149897, Melbourne, Australia

import tweepy
import couchdb
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
import _json
import json
import couchdb
import datetime
import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# couch = couchdb.Server("http://admin:000@127.0.0.1:5984")
# db = couch.create('tweet13')


API_key = config['twitter']['API_key']
API_secret = config['twitter']['API_secret']
Access_token = config['twitter']['Access_token']
Access_token_secret = config['twitter']['Access_token_secret']

auth = tweepy.OAuthHandler(API_key, API_secret)
auth.set_access_token(Access_token, Access_token_secret)

# Read in shape file
file=shapefile.Reader('GCCSA_2021_AUST_GDA2020.shp')
shapes=file.shapes() 
records=file.records() 

# Collect boundary of the suburbs
suburbId = [0,1,4,5,8,9,12,13,16,17,20]
suburbName = ["Flemington", "Carlton", "Docklands", "East Melbourne", "Kensington", "Melbourne", "North Melbourne", "Parkville", "Southbank", "Port Melbourne", "South Yarra - East"]

sub_plon = []
for i in range(len(shapes)):
    # Using the points information to draw the ploygon
    if i in suburbId:
        polygon = Polygon(shapes[i].points)
        sub_plon.append(polygon)

sub_info = list(zip(suburbName,sub_plon))

# nlp analyzer
analyzer = SentimentIntensityAnalyzer()

# Sentence analyzer
def sentimentanlyzer(sentence):
    sentiment = analyzer.polarity_scores(sentence)
    compound = sentiment['compound']
    if(compound>0.05):
        ## positive
        return "pos"
    elif(compound<=-0.05):
        ##negative
        return "neg"
    else:
        ##neutral
        return "neu"
    
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

stopwordsL = stopwordslist("stopwords.txt")

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)       
    return input_txt 

def analyzeContext(content):
    content = content.lower()
    words = [word for word in content.split() if word.lower() not in stopwordsL]
    content = " ".join(words)
    content = re.split('https:\/\/.*|http:\/\/.*',content)[0]
    content = remove_pattern(content, "@[\w]*")
    return content

def date_range(start, end):
    current = start
    while (end - current).days >= 0:
        yield current
        current = current + datetime.timedelta(seconds=1)

server = couchdb.Server("http://admin:admin@172.26.132.76:5984/")
db4 = server['all_tweets']
db1 = server['scenario1']
db2 = server['scenario2']
db3 = server['scenario3']
class MyStreamListener(tweepy.StreamListener):
    tweets = []
    limit = 100
    count = 0
    #db settings
    server = couchdb.Server("http://admin:admin@172.26.132.76:5984/")
    db4 = server['all_tweets']
    db1 = server['scenario1']
    db2 = server['scenario2']
    db3 = server['scenario3']

    def on_data(self, raw_data):
        keyWords1 = ["job", "employment", "recruit", "recruitment", "unemployment", "salary"]
        keyWords2 = ["education", "school", "teacher", "teachers", "student", "students", "study"]
        
        data = json.loads(raw_data)
        coord = data['coordinates']
        content = data['text']
        id = data['id']
        print(coord)
        if(coord):
            coord = coord["coordinates"]
            sub = None
            point = Point(coord[0],coord[1])
            for suburb in sub_info:
                # Return true if the point is in the ploygon
                if suburb[1].contains(point):
                    sub = suburb[0]
            print(sub)
            if(sub is not None):
                sent = analyzeContext(content)
                lan = data['lang']
                doc = {'suburb': sub, 'sentiment': sent, 'lan': lan}
                db4.save(doc)

                is_save = False
                for word in keyWords1:
                    if word in content:
                        doc ={'suburb': sub, 'sentiment': sent}
                        db1.save(doc)
                        is_save = True
                        break

                if(not is_save):
                    for word in keyWords2:
                        if word in content:
                            doc ={'suburb': sub, 'sentiment': sent}
                            db2.save(doc)
                            is_save = True
                            break

                if(not is_save):
                    doc = {'suburb': sub, 'lan': lan}
                    db3.save(doc)

    def on_status(self, status):
        self.count += 1
        if (self.count > self.limit):
            return False

    # returning False in on_error disconnects the stream ; #returning non-False reconnects the stream, with backoff.
    def on_error(self, status_code):
        if status_code == 420:
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

# keywords = ['covid']
bounding_box_melb = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]  # need to change

myStream.filter(locations=bounding_box_melb)
