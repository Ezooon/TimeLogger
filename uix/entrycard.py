from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from .tagchip import TagChip


Builder.load_file("uix/entrycard.kv")


class EntryCard(MDCard):
    entry = ObjectProperty()

    content = StringProperty("Empty Entry")
    timestamp = ObjectProperty(datetime.now())
    tags = ListProperty([])

    def on_entry(self, _, entry):
        self.content = entry.content
        self.timestamp = entry.timestamp
        self.tags = entry.tags

    def on_tags(self, _, tags):
        self.ids.tag_box.clear_widgets()
        for tag in tags:
            self.ids.tag_box.add_widget(TagChip(text=tag.tag))
