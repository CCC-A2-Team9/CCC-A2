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
file = shapefile.Reader('SA2_2016_AUST.shp')
shapes = file.shapes()
records = file.records()

# Collect boundary of the suburbs
suburbId = [692, 694, 695, 696, 698, 699, 700, 701, 703, 707, 714]
suburbName = ["Flemington", "Carlton", "Docklands", "East Melbourne", "Kensington", "Melbourne", "North Melbourne",
              "Parkville", "Southbank", "Port Melbourne", "South Yarra - East"]

sub_plon = []
for i in range(len(shapes)):
    # Using the points information to draw the ploygon
    if i in suburbId:
        polygon = Polygon(shapes[i].points)
        sub_plon.append(polygon)

sub_info = list(zip(suburbName, sub_plon))

# nlp analyzer
analyzer = SentimentIntensityAnalyzer()


# Sentence analyzer
def sentimentanlyzer(sentence):
    sentiment = analyzer.polarity_scores(sentence)
    compound = sentiment['compound']
    if (compound > 0.05):
        ## positive
        return "pos"
    elif (compound <= -0.05):
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
    content = re.split('https:\/\/.*|http:\/\/.*', content)[0]
    content = remove_pattern(content, "@[\w]*")
    return content


def date_range(start, end):
    current = start
    while (end - current).days >= 0:
        yield current
        current = current + datetime.timedelta(seconds=1)

db0 = server['all_tweets']
db1 = server['scenario1']
db2 = server['scenario2']
db3 = server['scenario3']
class MyStreamListener(tweepy.StreamListener):
    tweets = []
    limit = 100
    count = 0
    # db settings

    def on_data(self, raw_data):
        server = couchdb.Server("http://admin:admin@172.26.132.76:5984/")
        db0 = server['all_tweets']
        db1 = server['scenario1']
        db2 = server['scenario2']
        db3 = server['scenario3']
        keyWords1 = ["job", "employment", "recruit", "recruitment", "unemployment", "salary"]
        keyWords2 = ["education", "school", "teacher", "teachers", "student", "students", "study"]

        data = json.loads(raw_data)
        coord = data['coordinates']
        content = data['text']
        id = data['id']
        doc = {"id": id, "coord": coord, "content": content}
        db0.save(doc)
        if (coord):
            coord = coord["coordinates"]
            sub = None
            point = Point(coord[0], coord[1])
            for suburb in sub_info:
                # Return true if the point is in the ploygon
                if suburb[1].contains(point):
                    sub = sub[0]
            if (sub is not None):
                sent = analyzeContext(content)
                lan = data['lang']
                doc = {'suburb': sub, 'sentiment': sent, 'lan': lan}
                db0.save(doc)

                for word in keyWords1:
                    if word in content:
                        doc = {'suburb': sub, 'sentiment': sent}
                        print("save to db1")
                        db1.save(doc)
                        break

                for word in keyWords2:
                    if word in content:
                        doc = {'suburb': sub, 'sentiment': sent}
                        print("save to db2")
                        db2.save(doc)
                        break

                doc = {'suburb': sub, 'lan': lan}
                print("save to db3")
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
bounding_box_melb = [-124.7771694, 24.520833, -66.947028, 49.384472]  # need to change

myStream.filter(locations=bounding_box_melb)
