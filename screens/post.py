from datetime import date, datetime

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.pickers import MDDatePicker
from uix import PostCard

from database import Entry, wrap_dt

Builder.load_file("screens/post.kv")
today = datetime.today()


class PostScreen(MDBottomNavigationItem):
    view_data = ListProperty([])

    show_filters = BooleanProperty(False)

    from_date = ObjectProperty(date(year=today.year, month=today.month, day=today.day))
    to_date = ObjectProperty(today.replace(hour=23, minute=59, second=59, microsecond=0))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.re_add_tags = []

        self.date_dialog = MDDatePicker()

        Clock.schedule_once(self.setup, 0)

    def setup(self, _):
        self.load_posts()

    def load_posts(self, search_params=dict(), where=[], **kwargs):
        posts = Entry.table.get_items(
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
