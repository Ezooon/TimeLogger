import threading

from kivy.lang import Builder
from datetime import datetime
from socialapi import Twitter, LinkedIn, Facebook
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock, mainthread
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.app import App
from kivymd.uix.dialog import MDDialog

from .attachmentcard import AttachmentCard

Builder.load_file("uix/postcard.kv")

LinkedInButton = MDCheckbox(
    checkbox_icon_normal="linkedin",
    checkbox_icon_down="linkedin",
    active=True,
    ripple_alpha=0,
)
TwitterButton = MDCheckbox(
    checkbox_icon_normal="twitter",
    checkbox_icon_down="twitter",
    active=True,
    ripple_alpha=0,
)
FacebookButton = MDCheckbox(
    checkbox_icon_normal="facebook",
    checkbox_icon_down="facebook",
    active=True,
    ripple_alpha=0,
)


class PostCard(MDCard):
    post_dialog = None
    to_post_post = None
    """the postcard that the post_dialog will post when the post button is pressed"""

    post = ObjectProperty()

    content = StringProperty("Empty Entry")
    timestamp = ObjectProperty(datetime.now())
    attachments = ListProperty([])
    linkedin = BooleanProperty(False)
    twitter = BooleanProperty(False)
    facebook = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(args, **kwargs)
        if not PostCard.post_dialog:
            PostCard.post_dialog = MDDialog(
                title="Where to Post?",
                type="custom",
                content_cls=MDBoxLayout(size_hint=(1, None),
                                        height='50dp', pos_hint={"center_x": 0.5}),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=lambda _: PostCard.post_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Post",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: PostCard.send()
                    ),
                ],
            )
            PostCard.post_dialog.content_cls.add_widget(LinkedInButton)
            PostCard.post_dialog.content_cls.add_widget(TwitterButton)
            PostCard.post_dialog.content_cls.add_widget(FacebookButton)
            LinkedInButton.color_active = (0.7, 0.7, 1, 1)
            TwitterButton.color_active = (0.5, 0.5, 1, 1)
            FacebookButton.color_active = (0, 0, 1, 1)

            PostCard.post_dialog.update_width()
            PostCard.post_dialog.update_height()

    def open_post_dialog(self):
        PostCard.post_dialog.open()
        PostCard.to_post_post = self.post

    def on_post(self, _, post):
        self.content = post.content
        self.timestamp = post.timestamp
        self.attachments = post.attachments
        self.linkedin = post.linkedin
        self.twitter = post.twitter
        self.facebook = post.facebook

    def on_attachments(self, _, attachments):
        self.ids.attachment_box.clear_widgets()
        for attachment in attachments:
            self.ids.attachment_box.add_widget(AttachmentCard(attachment=attachment))

    @classmethod
    @mainthread
    def save_post(cls, post):
        post.save()
        App.get_running_app().root.ids.posts_screen.load_posts()

    @classmethod
    def send(cls):
        @mainthread
        def post_failed(error):
            toast(error)

        if LinkedInButton.active:
            threading.Thread(target=LinkedIn.post, args=(cls.to_post_post,
                                                         cls.save_post,
                                                         lambda e: mainthread(toast(
                                                             "Couldn't Post on LinkedIn Because:\n" + str(e))))).start()
        if TwitterButton.active:
            threading.Thread(target=Twitter.post, args=(cls.to_post_post,
                                                        cls.save_post,
                                                        lambda e: post_failed(
                                                            "Couldn't Post on Twitter Because:\n" + str(e)))).start()
        if FacebookButton.active:
            threading.Thread(target=Facebook.post, args=(cls.to_post_post,
                                                         cls.save_post,
                                                         lambda e: post_failed(
                                                             "Couldn't Post on Facebook Because:\n" + str(e)))).start()
        cls.post_dialog.dismiss()

    def edit(self):
        app = App.get_running_app()
        app.root.ids.posts_screen.edit_post(self.post)

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
