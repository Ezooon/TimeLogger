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
