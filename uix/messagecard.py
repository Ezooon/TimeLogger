from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder

Builder.load_file('./uix/messagecard.kv')


class MessageCard(MDBoxLayout):
    sender = StringProperty()

    content = StringProperty()

    def copy(self):
        Clipboard.copy(self.content)
        toast("Copied!")
