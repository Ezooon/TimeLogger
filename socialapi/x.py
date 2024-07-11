import tweepy
import json


with open("./apikeys.json", 'r') as f:
    keys = json.load(f)['x']

client = tweepy.Client(
    consumer_key=keys["api_key"], consumer_secret=keys["api_key_secret"],
    access_token=keys["access_token"], access_token_secret=keys["access_token_secret"]
)

auth = tweepy.OAuthHandler(keys["api_key"], keys["api_key_secret"])
auth.set_access_token(keys["access_token"], keys["access_token_secret"])
api = tweepy.API(auth)


m = api.media_upload("E:\\Workspace\\projects\\TimeLogger\\assets\\file.png")

client.create_tweet(text="Hello World! from tweepy", media_ids=[m.media_id])

# public_tweets = api.update_status("A test post using tweepy! #buildinpublic")

# for tweet in public_tweets:

# print(public_tweets)