from kivymd.app import MDApp
from kivy.properties import BooleanProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton


class SM(MDScreenManager):
    pass


class TimeLogger(MDApp):
    undo = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snackbar = None

    def build(self):
        self.title = "Time Logger"
        self.icon = "assets/logo.png"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.material_style = "M2"

        self.setup_undo_snakbar()
        return SM()

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


TimeLogger().run()

from database.db_api import db_api
db_api.close()
