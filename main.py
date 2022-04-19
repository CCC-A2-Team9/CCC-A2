import tweepy
import couchdb
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
import json
import couchdb
couch = couchdb.Server("http://admin:0000@127.0.0.1:5984")
db = couch.create('tweet9')


API_key = config['twitter']['API_key']
API_secret = config['twitter']['API_secret']
Access_token = config['twitter']['Access_token']
Access_token_secret = config['twitter']['Access_token_secret']


auth = tweepy.OAuthHandler(API_key, API_secret)
auth.set_access_token(Access_token, Access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print(tweepy.__version__)

places = api.geo_search(query="Melbourne -filter:retweets", granularity="city")
print(places)
for place in places:
    print("placeid:%s" % place)

tweets_list1 = tweepy.Cursor(api.search, count=100,q="place:%s" % place.id,since="2021-01-01",show_user = True,tweet_mode="extended").items()
for tweet in tweets_list1:
    print(tweet)
query="covid -is:retweets"
tweets_list2 = tweepy.Cursor(api.search, query=query,geocode="-37.999250,144.997395,57km",since="2021-01-01",show_user = True,tweet_mode="extended").items(10)
# for tweet in tweets_list2:
#     print(tweet)
# tweets_list1 = tweepy.Cursor(api.search, count=100, q="place:%s" % place.id, since="2021-01-01", show_user=True,
#                              tweet_mode="extended").items()
count=1
for tweet in tweets_list2:
    tson = tweet._json
    id = tson['id']
    content = tson['full_text']
    doc = {id:content}
    db.save(doc)
    count+=1
print(count)



