from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from utils import resource_path

Builder.load_file(resource_path('uix/settings.kv'))


class DropDownSetting(MDCard):
    setting = StringProperty("Setting")

    options = ListProperty(["One", "Two"])

    selected_option = StringProperty("One")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": option,
                "on_release": lambda x=option: self.menu_callback(x),
            } for option in self.options
        ]
        self.menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
        )

    def on_options(self, _, options):
        self.selected_option = options[0]
        menu_items = [
            {
                "text": option,
                "on_release": lambda x=option: self.menu_callback(x),
            } for option in options
        ]

        self.menu.caller = self.ids.selected_option
        self.menu.items = menu_items

    def menu_callback(self, option):
        self.selected_option = option
        self.menu.dismiss()

    def on_release(self):
        self.menu.open()
