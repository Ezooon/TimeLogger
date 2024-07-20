from kivy.lang import Builder
from kivy.app import App
from kivymd.toast import toast
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

Builder.load_file("screens/preferences.kv")


class PreferencesScreen(MDBottomNavigationItem):
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
