import tweepy
from os import path
import webbrowser


class TwitterAPI:
    def __init__(self, api_key, api_key_secret, access_token=None, access_token_secret=None):
        self.api = None
        self.client = None
        self.auth = tweepy.OAuthHandler(api_key, api_key_secret, access_token, access_token_secret)

        self.login()

    def login(self):
        if not self.auth.access_token: return
        
        self.client = tweepy.Client(consumer_key=self.auth.consumer_key,
                                    consumer_secret=self.auth.consumer_secret,
                                    access_token=self.auth.access_token,
                                    access_token_secret=self.auth.access_token_secret)

        self.auth.set_access_token(self.auth.access_token, self.auth.access_token_secret)
        self.api = tweepy.API(self.auth)

    def logout(self):
        self.client = None
        self.auth.set_access_token(None, None)
        self.api = None

    def authorize_login(self):
        try:
            auth_url = self.auth.get_authorization_url()
            webbrowser.open(auth_url)
        except Exception as e:
            print('Error! Failed to get access token. \ne')

    def get_access_token(self, oauth_token, oauth_token_secret):
        try:
            self.auth.request_token['oauth_token'] = oauth_token
            self.auth.request_token['oauth_token_secret'] = oauth_token_secret
            self.auth.access_token, self.auth.access_token_secret = self.auth.get_access_token(oauth_token_secret)
            self.login()
            return self.auth.access_token, self.auth.access_token_secret
        except Exception as e:
            print('Error! Failed to get access token. \ne')

    def post(self, post, on_success, on_failure):
        try:
            media_ids = []
            for att in post.attachments:
                if path.exists(att.path):
                    media_ids.append(self.api.media_upload(att.path).media_id)

            self.client.create_tweet(text=post.content, media_ids=media_ids or None)
            post.twitter = True
            on_success(post)

        except Exception as e:
            on_failure(e)


