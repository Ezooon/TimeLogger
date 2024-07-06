from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.app import App

from .attachmentcard import AttachmentCard
from .tagchip import TagChip

Builder.load_file("uix/entrycard.kv")


class EntryCard(MDCard):
    entry = ObjectProperty()

    content = StringProperty("Empty Entry")
    timestamp = ObjectProperty(datetime.now())
    tags = ListProperty([])
    attachments = ListProperty([])

    def on_entry(self, _, entry):
        self.content = entry.content
        self.timestamp = entry.timestamp
        self.tags = entry.tags
        self.attachments = entry.attachments

    def on_tags(self, _, tags):
        self.ids.tag_box.clear_widgets()
        for tag in tags:
            self.ids.tag_box.add_widget(TagChip(tag=tag))

    def on_attachments(self, _, attachments):
        self.ids.attachment_box.clear_widgets()
        for attachment in attachments:
            self.ids.attachment_box.add_widget(AttachmentCard(attachment=attachment))

    def edit(self):
        app = App.get_running_app()
        app.root.ids.entries_screen.edit_past_entry(self.entry)

    def delete(self):
        app = App.get_running_app()
        load = app.root.ids.entries_screen.load_entries
        load(where=[("id", "not in", f"({self.entry.id})")])
        entry = self.entry
        app.snackbar.open()

        def permanent_delete(_):
            if not app.undo:
                print("deleteing: ", entry)
                entry.delete()
            else:
                load()
            app.undo = False

        Clock.schedule_once(permanent_delete, 3)
