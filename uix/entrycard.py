from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.app import App
from utils import resource_path

from .attachmentcard import AttachmentCard
from .tagchip import TagChip

Builder.load_file(resource_path("uix/entrycard.kv"))


class EntryCard(MDCard):
    entry = ObjectProperty()

    content = StringProperty("Empty Entry")
    timestamp = ObjectProperty(datetime.now())
    tags = ListProperty([])
    attachments = ListProperty([])

    # excluded = BooleanProperty(False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, **kwargs)
    #     app = App.get_running_app()
    #     app.root.ids.entries_screen.bind(excluded_entries=self.is_excluded)

    def on_entry(self, _, entry):
        self.content = entry.content
        self.timestamp = entry.timestamp
        self.tags = entry.tags
        self.attachments = entry.attachments

        # app = App.get_running_app()
        # self.is_excluded(None, app.root.ids.entries_screen.excluded_entries)

    def on_tags(self, _, tags):
        self.ids.tag_box.clear_widgets()
        for tag in tags:
            self.ids.tag_box.add_widget(TagChip(tag=tag))

    def on_attachments(self, _, attachments):
        self.ids.attachment_box.clear_widgets()
        for attachment in attachments:
            self.ids.attachment_box.add_widget(AttachmentCard(attachment=attachment))

    def is_excluded(self, _, entries):
        if self in entries:
            self.excluded = True
        else:
            self.excluded = False

    # def exclude(self):
    #     app = App.get_running_app()
    #     app.root.ids.entries_screen.excluded_entries.append(self)

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
                entry.delete()
            else:
                load()
            app.undo = False

        Clock.schedule_once(permanent_delete, 3)
