from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager


class SM(MDScreenManager):
    pass


class TimeLogger(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.material_style = "M2"
        return SM()


TimeLogger().run()
