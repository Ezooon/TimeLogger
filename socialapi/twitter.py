import tweepy
import json
from os import path

with open("socialapi/apikeys.json", 'r') as f:
    keys = json.load(f)['x']


class TwitterAPI:
    def __init__(self, bearer_token, consumer_key, consumer_secret, access_token, access_token_secret):
        self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

        self.auth = tweepy.OAuthHandler(keys["api_key"], keys["api_key_secret"])
        self.auth.set_access_token(keys["access_token"], keys["access_token_secret"])
        self.api = tweepy.API(self.auth)

    def post(self, post, on_success, on_failure):
        try:
            media_ids = []
            for att in post.attachments:
                if path.exists(att.path):
                    media_ids.append(self.api.media_upload(att.path).media_id)
            self.client.create_tweet(text=post.content, media_ids=media_ids)
            post.twitter = True
            on_success(post)
        except Exception as e:
            on_failure(e)


Twitter = TwitterAPI(
    bearer_token=keys["bearer_token"],
    consumer_key=keys["api_key"], consumer_secret=keys["api_key_secret"],
    access_token=keys["access_token"], access_token_secret=keys["access_token_secret"])
