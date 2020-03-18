import tweepy
from pymongo import MongoClient
import datetime
# Authenticate to Twitter
auth = tweepy.OAuthHandler("8vw2LMZcr4wOTBkO37y8GWIy6",
                           "gO9zj0YeoSEFzwkqWF11v0jQQdlhz0jBX3qmE2ePMWU1V3Mx5t")
auth.set_access_token("2173337422-eTfIbtZa5a9ghDo1vPdRLOHaqieDBsXssECKP0J",
                      "JAdECP1xSqdq2AnBOrP8hZJkJyMqwaObehRTFxhdJXg6a")


# MongoDB Database connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client.webscience
collection = db['tweets']

# Create API object
api = tweepy.API(auth)


# REST API calls
rest = api.search(['president', 'trump', 'whitehouse'], lang=["en"])


for item in rest:

    tweetID = item['id_str']  # Print the Tweet ID
    # Print username of the Tweet author
    username = item['user']['screen_name']
    # Print no of people who follow tweet author
    followers = item['user']['followers_count']
    text = item['text']  # Print the text of the tweet
    hashtags = item['entities']['hashtags']  # Hashtags of the Tweet
    timestamp = item['created_at']  # Tweet timestamp

    # Convert timestamp so that it can be read by MongoDB
    created = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')

    tweetDoc = {'id':tweetID, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'created':created}
    db.tweets.insert_one(tweetDoc)




# Create a tweet

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweetID = status._json['id_str']  # Print the Tweet ID
        username = status._json['user']['screen_name']  # Print username of the Tweet author
        followers = status._json['user']['followers_count']  # Print no of people who follow tweet author
        text = status._json['text']  # Print the text of the tweet
        hashtags = status._json['entities']['hashtags']  # Hashtags of the Tweet
        timestamp = status._json['created_at']  # Tweet timestamp

        # Convert timestamp so that it can be read by MongoDB
        created = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')

        tweetDoc = {'id':tweetID, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'created':created}
        db.tweets.insert_one(tweetDoc)





myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['president', 'trump', 'whitehouse'], languages=["en"])
