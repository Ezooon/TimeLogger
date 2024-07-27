import json
import threading
from datetime import time
from os import path, environ

from cryptography.fernet import Fernet

from kivy.properties import BooleanProperty, ObjectProperty, DictProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton

from socialapi import TwitterAPI, FacebookAPI, LinkedInAPI
from starlette.responses import HTMLResponse
from continuous_logging.schedule import schedule_continuous_logging

from uvicorn import run
from fastapi import FastAPI

user_key = Fernet(environ.get("user_key"))
app_key = Fernet(environ.get("app_key"))
asgi_app = FastAPI()


class SM(MDScreenManager):
    pass


class TimeLogger(MDApp):
    undo = BooleanProperty(False)

    linkedin = ObjectProperty(None)
    logged_in_linkedin = BooleanProperty(False)

    twitter = ObjectProperty(None)
    logged_in_twitter = BooleanProperty(False)

    facebook = ObjectProperty(None)
    logged_in_facebook = BooleanProperty(False)

    con_log = DictProperty({
            'action': 'Notification',
            'often': 'Multiple Times a Day',
            'repetition': 'Every Hour',
            'when': time(hour=21)
        })

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snackbar = None

    def build_config(self, config):
        config.setdefaults('Theme', {'style': 'Dark'})
        config.setdefaults('Post', {
            'num': 2,
            'area': 'Live update',
            'tone': 'casual',
            'note': '',
            'keywords': '',
            'hashtags': '#timelogger'
        })
        config.setdefaults("Continuous Logging", self.con_log)

    def build(self):
        self.title = "Time Logger"
        self.icon = "assets/logo.png"
        self.theme_cls.theme_style = self.config.get('Theme', 'style')
        self.theme_cls.primary_palette = "Yellow"  # 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow',
        # 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.material_style = "M2"

        self.login()

        self.setup_undo_snakbar()

        self.load_continuous_logging_options()

        return SM()

    def login(self):
        keys = self.get_keys()
        user_data = self.get_user_data()

        self.linkedin = LinkedInAPI(
            keys["linkedin"].get("client_id"),
            keys["linkedin"].get("client_secret"),
            user_data["linkedin"].get("user_id"),
            user_data["linkedin"].get("access_token"),
        )
        self.logged_in_linkedin = bool(user_data['linkedin'].get("access_token"))

        self.twitter = TwitterAPI(api_key=keys["x"].get("api_key"),
                                  api_key_secret=keys["x"].get("api_key_secret"),
                                  access_token=user_data["x"].get("access_token"),
                                  access_token_secret=user_data["x"].get("access_token_secret"))
        self.logged_in_twitter = bool(user_data["x"].get("access_token"))

        self.facebook = FacebookAPI(
            keys["facebook"].get("client_id"),
            keys["facebook"].get("client_secret"),
            user_data["facebook"].get("page_id"),
            user_data["facebook"].get("access_token"),
        )
        self.logged_in_facebook = bool(user_data['facebook'].get("access_token"))

    def setup_undo_snakbar(self):
        self.snackbar = MDSnackbar(auto_dismiss=False)
        # self.snackbar.size_hint_x = (Window.width - (self.snackbar.snackbar_x * 2)) / Window.width
        self.snackbar.add_widget(MDLabel(text="Undo Deletion?", adaptive_height=True))
        self.snackbar.add_widget(MDSnackbarActionButton(
            text="Undo",
            text_color=self.theme_cls.primary_color,
            theme_text_color="Custom",
            font_style="Button",
            on_press=lambda *_: setattr(self, "undo", True),
            on_release=self.snackbar.dismiss,
        ))

    def get_keys(self):
        with open('socialapi/keys.data', 'rb') as f:
            keys = f.read()
        keys = json.loads(app_key.decrypt(keys.decode()).decode())

        # use the commented code to modify keys.data
        # with open('socialapi/keys.data', 'wb') as f:
        #     f.write(app_key.encrypt(json.dumps(keys).encode()))

        return keys

    def get_user_data(self):
        if not path.exists('user_data.data'):
            data = json.dumps({
                "x": {
                    "access_token": None,
                    "access_token_secret": None
                },
                "linkedin": {
                    "user_id": None,
                    "access_token": None
                },
                "facebook": {
                    "page_id": None,
                    "access_token": None
                }
            })
            user_data = user_key.encrypt(data.encode())
            with open('user_data.data', 'wb') as f:
                f.write(user_data)

        with open("user_data.data", 'r') as f:
            user_data = user_key.decrypt(f.read()).decode()

        return json.loads(user_data)

    def save_user_data(self):
        data = json.dumps({
            "x": {
                "access_token": self.twitter.auth.access_token,
                "access_token_secret": self.twitter.auth.access_token_secret
            },
            "linkedin": {
                "user_id": self.linkedin.user_id,
                "access_token": self.linkedin.access_token
            },
            "facebook": {
                "page_id": self.facebook.page_id,
                "access_token": self.facebook.access_token
            }
        })
        user_data = user_key.encrypt(data.encode())
        with open('user_data.data', 'wb') as f:
            f.write(user_data)

    def load_continuous_logging_options(self):
        self.con_log = {
            'action': self.config.get('Continuous Logging', 'action'),
            'often': self.config.get('Continuous Logging', 'often'),
            'repetition': self.config.get('Continuous Logging', 'repetition'),
            'when': time.fromisoformat(self.config.get('Continuous Logging', 'when')),
        }

    def save_continuous_logging_options(self):
        action = self.con_log['action']
        often = self.con_log['often']
        repetition = self.con_log['repetition']
        when = self.con_log['when']
        # try:
        schedule_continuous_logging(action, often, repetition, when)

        self.config.set('Continuous Logging', 'action', action)
        self.config.set('Continuous Logging', 'often', often)
        self.config.set('Continuous Logging', 'repetition', repetition)
        self.config.set('Continuous Logging', 'when', when)

        self.config.write()
        # except:
        #     toast("Restart the Application as Administrator")
        #     self.load_continuous_logging_options()


app = TimeLogger()


@asgi_app.get("/x/")
def twitter_login(oauth_token, oauth_verifier):
    app.twitter.get_access_token(oauth_token, oauth_verifier)
    app.logged_in_twitter = True
    app.save_user_data()
    return HTMLResponse("Return to Time Logger")


@asgi_app.get("/linkedin/")
def linkedin_login(code, state):
    app.logged_in_linkedin = app.linkedin.get_access_token(code, state) is not None
    app.save_user_data()
    return HTMLResponse("Return to Time Logger")


@asgi_app.get("/facebook/")
def facebook_login(token, expires_in):
    app.facebook.get_access_token(token, expires_in)
    app.logged_in_facebook = True
    app.save_user_data()
    return HTMLResponse("Return to Time Logger")


server_thread = threading.Thread(target=run, args=(asgi_app,), kwargs={"host": "127.0.0.1", "port": 7888}, daemon=True)
server_thread.start()
app.run()
from database.db_api import db_api
db_api.close()
