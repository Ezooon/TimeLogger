import requests
import webbrowser
from random import randint


class LinkedInAPI:
    def __init__(self, client_id, client_secret, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        self.state = randint(10000, 99999)
        # a random number to ensure the user wants to log in from the app

        self.login()

    def login(self):
        pass

    def logout(self):
        self.access_token = None

    def post(self, post, on_success, on_failure):
        api_url = 'https://api.linkedin.com/v2/ugcPosts'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/json',
        }

        post_body = {
            'author': f'urn:li:person:{self.client_id}',
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': post.content,
                    },
                    # 'shareMediaCategory': 'ARTICLE',
                    # 'media': [
                    #     {
                    #         'status': 'READY',
                    #         'description': {
                    #             'text': 'Read our latest blog post about LinkedIn API!',
                    #         },
                    #         'originalUrl': '<your_blog_post_url>',
                    #     },
                    # ],
                },
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
            },
        }

        response = requests.post(api_url, headers=headers, json=post_body)
        if response.status_code == 201:
            on_success(post)
        else:
            on_failure(f'{response.status_code}: {response.text}')
            
    def authorize_login(self):
        webbrowser.open(
            f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id="
            f"{self.client_id}&redirect_uri=http://localhost:7888/linkedin/&state={self.state}&scope=w_member_social")

    def get_access_token(self, code, state):
        print(state != self.state, state, self.state)
        # if state != self.state:
        #     return  # ToDo raise an exception

        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:7888/linkedin/',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(url, data=params)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.login()
            return self.access_token
        else:  # ToDo raise an exception
            print('Error:', response.status_code, response.text)

