from kivy.app import App
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from utils import resource_path

Builder.load_file(resource_path("screens/preferences.kv"))


class PreferencesScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time_picker = MDTimePicker()
        self.time_picker.on_save = self.ok

    def ok(self, picked_time):
        app = App.get_running_app()
        self.time_picker.dismiss()
        app.con_log['when'] = picked_time
        app.save_continuous_logging_options()

    def open_time_picker(self):
        self.time_picker.set_time(App.get_running_app().con_log['when'])
        self.time_picker.text_color = 0,0,0,1
        self.time_picker.input_field_text_color = 0,0,0,1
        self.time_picker.open()

    def change_theme_style(self, dark):
        app = App.get_running_app()
        s = 'Dark' if dark else 'Light'
        app.theme_cls.theme_style = s
        app.config.set('Theme', 'style', s)
        app.config.write()
        toast("restart")

    def facebook_login(self):
        app = App.get_running_app()
        app.facebook.authorize_login()

    def facebook_logout(self):
        app = App.get_running_app()
        app.facebook.logout()
        app.logged_in_facebook = False
        app.save_user_data()

    def twitter_login(self):
        app = App.get_running_app()
        app.twitter.authorize_login()

    def twitter_logout(self):
        app = App.get_running_app()
        app.twitter.logout()
        app.logged_in_twitter = False
        app.save_user_data()

    def linkedin_login(self):
        app = App.get_running_app()
        app.linkedin.authorize_login()

    def linkedin_logout(self):
        app = App.get_running_app()
        app.linkedin.logout()
        app.logged_in_linkedin = False
        app.save_user_data()
