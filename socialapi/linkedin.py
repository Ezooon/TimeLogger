import json
import requests
import webbrowser
from random import randint
from os.path import exists


class LinkedInAPI:
    def __init__(self, client_id, client_secret, user_id=None, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.access_token = access_token

        # a random number to ensure the user wants to log in from the app

        self.login()

    def login(self):
        if self.access_token:
            self.get_user_id()

    def logout(self):
        self.access_token = None

    def post(self, post, on_success, on_failure):
        if not self.access_token:
            on_failure("Log In First")
            return
        if not self.user_id:
            if self.get_user_id():
                on_failure("Connection Error")
                return

        api_url = 'https://api.linkedin.com/v2/ugcPosts'

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Connection': 'Keep-Alive',
            'Linkedin-Version': "format AAAAMM",
            "X-Restli-Protocol-Version": '2.0.0',
            'Content-Type': 'application/json',
        }

        if post.attachments:
            image_upload_endpoint = "https://api.linkedin.com/v2/assets?action=upload"
            upload_headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/octet-stream"
            }
            images_ids = []
            exceptions = []

            # Set the image file path and upload it to LinkedIn
            for image_file_path in post.attachments:
                if exists(image_file_path.path):
                    try:
                        payload = {
                            "registerUploadRequest": {
                                "owner": f"urn:li:person:{self.user_id}",
                                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                                "serviceRelationships": [
                                    {
                                        "identifier": "urn:li:userGeneratedContent",
                                        "relationshipType": "OWNER"
                                    }
                                ]
                            }
                        }
                        register_post = requests.post(
                            f"https://api.linkedin.com/v2/assets?action=registerUpload&oauth2_access_token={self.access_token}",
                            json=payload
                        ).json()
                        print(register_post['value']['asset'])
                        upload_url = register_post['value']['uploadMechanism'][
                            'com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']

                        image_upload_response = requests.post(upload_url, headers=upload_headers,
                                                              data=open(image_file_path.path, "rb"))
                        images_ids.append(register_post['value']['asset'])
                    except Exception as e:
                        exceptions.append(e)

            if exceptions: print(exceptions)

            # Set the post data
            post_body = {
                "author": f"urn:li:person:{self.user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            # "id": "urn:li:share:your_share_id",
                            "text": post.content
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [{
                                        "status": "READY",
                                        "media": img_id,
                                    } for img_id in images_ids]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }}

        else:
            post_body = {
                "author": f"urn:li:person:{self.user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": post.content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility":  {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

        response = requests.post(api_url, headers=headers, json=post_body)
        if response.status_code == 201:
            post.linkedin = True  # ToDo save the post id into this field.
            on_success(post)
        else:
            on_failure(f'{response.status_code}: {response.text}')
            
    def authorize_login(self):
        webbrowser.open(
            f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id="
            f"{self.client_id}&redirect_uri=http://localhost:7888/linkedin/&"
            "scope=w_member_social%20openid%20email%20profile")

    def get_access_token(self, code):
        try:
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
                return print(f'{response.status_code}: {response.text}')
        except Exception as e:
            print(e)

    def get_user_id(self):
        # url = "https://api.linkedin.com/v2/me"
        url = "https://api.linkedin.com/v2/userinfo"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(url, headers=headers)
            user_data = response.json()
            self.user_id = user_data.get("sub")  # ToDo raise an Exeption
            return self.user_id
        except Exception as e:
            return False
