import json
import threading
from datetime import date, datetime

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty
from kivymd.toast import toast
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from utils import resource_path
from aitool import generate

from database import Post, wrap_dt


Builder.load_file(resource_path("screens/post.kv"))
today = datetime.today()


class PostScreen(MDBottomNavigationItem):
    view_data = ListProperty([])

    show_filters = BooleanProperty(False)

    from_date = ObjectProperty(date(year=today.year, month=today.month, day=today.day))
    to_date = ObjectProperty(today.replace(hour=23, minute=59, second=59, microsecond=0))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.generate_dialog = MDDialog(
            title="Generate New Post",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                adaptive_height=True
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda _: self.generate_dialog.dismiss()
                ),
                MDFlatButton(
                    text="Generate",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda _: self.start_generating()
                ),
            ],
        )
        self.gen_num_field = MDTextField(
            hint_text="Number of Posts",
            input_filter="int",
            text=app.config.get('Post', 'num'),
            required=True
        )
        self.generate_dialog.content_cls.add_widget(self.gen_num_field)
        self.gen_area_field = MDTextField(
            hint_text="Area or Niche",
            text=app.config.get('Post', 'area'),
            required=True
        )
        self.generate_dialog.content_cls.add_widget(self.gen_area_field)
        self.gen_tone_field = MDTextField(
            hint_text="Tone",
            text=app.config.get('Post', 'tone'),
            required=True
        )
        self.generate_dialog.content_cls.add_widget(self.gen_tone_field)
        self.gen_note_field = MDTextField(
            hint_text="Note",
            text=app.config.get('Post', 'note'),
            helper_text="Any thing you want the LLM to consider"
        )
        self.generate_dialog.content_cls.add_widget(self.gen_note_field)
        self.gen_keywords_field = MDTextField(
            hint_text=app.config.get('Post', 'keywords'),
        )
        self.generate_dialog.content_cls.add_widget(self.gen_keywords_field)
        self.gen_hashtags_field = MDTextField(
            hint_text="Hashtags",
            text=app.config.get('Post', 'hashtags'),
        )
        self.generate_dialog.content_cls.add_widget(self.gen_hashtags_field)

        self.re_add_tags = []

        self.date_dialog = MDDatePicker()

        Clock.schedule_once(self.setup, 0)

    def setup(self, _):
        self.load_posts()

    def load_posts(self, search_params=dict(), where=[], **kwargs):
        posts = Post.table.get_items(
            search_params={"content": self.ids.search_field.text, **search_params},
            where=where + [
                    ("timestamp", ">", wrap_dt(self.from_date)),
                    ("timestamp", "<", wrap_dt(self.to_date)),
                  ],
            **kwargs
        )

        self.view_data = [{
            "viewclass": "PostCard",
            "post": post,
            "size_hint": (1, None),
        } for post in posts]

        self.ids.sv.scroll_y = 0
        Clock.schedule_once(self.ids.sv.refresh_from_data, 0)

    def show_date_picker(self, to=True):
        if to:
            d = self.to_date
        else:
            d = self.from_date

        self.date_dialog.sel_day = d.day
        self.date_dialog.update_calendar(d.year, d.month)

        self.date_dialog.open()

        def ok(_to, picked_date, _):
            if _to:
                self.to_date = datetime(year=picked_date.year, month=picked_date.month, day=picked_date.day,
                                        hour=23, minute=59, second=59, microsecond=0)
                self.ids.to_date_picker.text = "To: " + str(self.to_date.date())
            else:
                self.from_date = picked_date
            self.date_dialog.dismiss()
            self.load_posts()

        self.date_dialog.on_save = lambda *args: ok(to, *args)

    def start_generating(self):
        self.ids.gen_button.icon = "timer-sand"

        num = self.gen_num_field.text
        area = self.gen_area_field.text
        tone = self.gen_tone_field.text
        if not all([num, area, tone]):
            return

        note = self.gen_note_field.text
        keywords = self.gen_keywords_field.text
        hashtags = self.gen_hashtags_field.text

        app = App.get_running_app()
        entries = [entry_card["entry"] for entry_card in app.root.ids.entries_screen.view_data]

        threading.Thread(
            target=generate,
            args=(entries, num, area, tone, note, keywords, hashtags, self.add_posts, self.generation_failure)
        ).start()
        self.generate_dialog.dismiss()

        app.config.set('Post', 'num', num)
        app.config.set('Post', 'area', area)
        app.config.set('Post', 'tone', tone)
        app.config.set('Post', 'note', note)
        app.config.set('Post', 'keywords', keywords)
        app.config.set('Post', 'hashtags', hashtags)
        app.config.write()

    @mainthread
    def add_posts(self, posts_json: str):
        self.ids.gen_button.icon = "creation-outline"
        try:
            posts = json.loads(posts_json)

            if isinstance(posts, list):
                for post in posts:
                    Post(content=post["content"], attachments=post["suggested images"]).save()
            else:
                Post(content=posts["content"], attachments=posts["suggested images"]).save()
        except:
            toast("AI failure! Try again.")

        self.load_posts()

    def edit_post(self, post):
        entries_screen = self.parent.get_screen("entries_screen")
        entries_screen.entry_edit = False
        entries_screen.editing_post = post
        entries_screen.ids.edit_field.text = post.content
        entries_screen.ids.tag_box.clear_widgets()
        entries_screen.ids.attachment_box.clear_widgets()
        entries_screen.add_attachments(post.attachments)

        self.parent.switch_to(entries_screen)
        Clock.schedule_once(lambda _: entries_screen.animate_edit_card(), 0)

    def generation_failure(self, excep):
        Clock.schedule_once(lambda x: toast("couldn't generate posts"), 0)
        self.ids.gen_button.icon = "creation-outline"

