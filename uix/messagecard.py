from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file('./uix/messagecard.kv')


class MessageCard(MDBoxLayout):
    sender = StringProperty()

    content = StringProperty()
