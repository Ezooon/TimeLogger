import facebook
import webbrowser
from os.path import exists


class FacebookAPI:
    def __init__(self, client_id, client_secret, page_id=None, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.page_id = page_id
        self.access_token = access_token

        self.api = facebook.GraphAPI(self.access_token)

    def login(self):
        # Create a Facebook Graph API object
        self.api = facebook.GraphAPI(self.access_token)

    def logout(self):
        self.access_token = None
        self.api = facebook.GraphAPI(self.access_token)

    def post(self, post, on_success, on_failure):
        try:
            if post.attachments:
                media_ids = []
                for att in post.attachments:  # ToDo I should probably make sure it's an Image.
                    if exists(att.path):
                        media_ids.append(self.api.put_photo(
                            image=open(att.path, 'rb')))  # , message='', profile_id='profile/page id'))
                print(media_ids)
            else:
                post_id = self.api.put_wall_post("Hello, world!")  # ToDo store the post id
        except Exception as e:
            on_failure(e)

    def authorize_login(self):
        try:
            auth_url = self.api.get_auth_url(self.client_id, None)  # "http://127.0.0.1:7888/facebook/")
            webbrowser.open(auth_url)
        except Exception as e:
            print('Error! Failed to get access token. \ne')

    def get_access_token(self, token, expires_in):
        self.access_token = token
        self.login()
        self.api.extend_access_token(self.client_id, self.client_secret)




