from kivy.lang import Builder
from datetime import datetime
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App

from .attachmentcard import AttachmentCard
from .tagchip import TagChip

Builder.load_file("uix/postcard.kv")


class PostCard(MDCard):
    post = ObjectProperty()

    content = StringProperty("Empty Entry")
    timestamp = ObjectProperty(datetime.now())
    attachments = ListProperty([])

    def on_post(self, _, post):
        self.content = post.content
        self.timestamp = post.timestamp
        self.attachments = post.attachments

    def on_attachments(self, _, attachments):
        self.ids.attachment_box.clear_widgets()
        for attachment in attachments:
            self.ids.attachment_box.add_widget(AttachmentCard(attachment=attachment))

    def send(self):
        pass

    def delete(self):
        app = App.get_running_app()
        load = app.root.ids.posts_screen.load_posts
        load(where=[("id", "not in", f"({self.post.id})")])
        post = self.post
        app.snackbar.open()

        def permanent_delete(_):
            if not app.undo:
                post.delete()
            else:
                load()
            app.undo = False

        Clock.schedule_once(permanent_delete, 3)
