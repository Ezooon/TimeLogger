from kivy.clock import Clock
from kivy.lang import Builder
from datetime import date, datetime
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, DictProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.pickers import MDDatePicker
from plyer import filechooser
from utils import resource_path
from database import Entry, Post, wrap_dt, Attachment, Tag
from uix import TagChip, AttachmentCard

Builder.load_file(resource_path("screens/entries.kv"))
today = date.today()


class EntriesScreen(MDBottomNavigationItem):
    view_data = ListProperty([])

    entry_edit = BooleanProperty(True)
    show_filters = BooleanProperty(False)

    filter_with = DictProperty()
    filter_out = DictProperty()

    from_date = ObjectProperty(date.today())
    to_date = ObjectProperty(datetime.today().replace(hour=23, minute=59, second=59, microsecond=0))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editing_post = None
        self.editing_entry = None

        self.re_add_tags = []

        self.date_dialog = MDDatePicker()

        self.attach = lambda *_: filechooser.open_file(title="Pick a File", preview=True, on_selection=self.add_attachment,)

        Clock.schedule_once(self.setup, 0)

    def setup(self, _):
        self.ids.edit_field.bind(text=self.on_edit_field_text)
        self.load_entries()
        self.load_tags()

    def load_tags(self):
        self.filter_with = dict()
        self.filter_out = dict()
        self.ids.filter_tag_box.clear_widgets()
        Tag.table.update_all()

        def on_press(tagc):
            tag_name = tagc.tag.tag
            # filter out red
            if tag_name in self.filter_with:
                self.filter_out[tag_name] = self.filter_with.pop(tag_name)
                tagc.tag_color = self.theme_cls.error_color
                tagc.text_color = self.theme_cls.text_color

            # dont filter gray
            elif tag_name in self.filter_out:
                self.filter_out.pop(tag_name)
                tagc.tag_color = "#44444499"
                tagc.text_color = self.theme_cls.opposite_text_color
                if not self.show_filters:
                    self.ids.filter_tag_box.remove_widget(tagc)
                    self.ids.filter_tag_box.add_widget(tagc)
                else:
                    if tagc in self.re_add_tags:
                        self.re_add_tags.remove(tagc)

            # filter with green
            else:
                self.filter_with[tag_name] = tagc.tag
                tagc.tag_color = "#00ff00"
                tagc.text_color = self.theme_cls.opposite_text_color
                if not self.show_filters:
                    self.ids.filter_tag_box.remove_widget(tagc)
                    self.ids.filter_tag_box.add_widget(tagc, len(self.ids.filter_tag_box.children))
                else:
                    self.re_add_tags.append(tagc)

            # so the filters don't update while choosing tags
            if not self.show_filters:
                self.load_entries()

        for key, tag in Tag.table.all.items():
            self.ids.filter_tag_box.add_widget(TagChip(
                tag=tag,
                on_press=on_press,
                tag_color="#44444499"))

    def load_entries(self, search_params=dict(), where=[], **kwargs):
        entries = Entry.table.get_items(
            search_params={"content": self.ids.search_field.text, **search_params},
            where=where + [
                    ("timestamp", ">", wrap_dt(self.from_date)),
                    ("timestamp", "<", wrap_dt(self.to_date)),
                  ],
            tags_in=tuple(t.id for _, t in self.filter_with.items()),
            tags_out=tuple(t.id for _, t in self.filter_out.items()),
            **kwargs
        )

        self.view_data = [{
            "viewclass": "EntryCard",
            "entry": entry,
            "size_hint": (1, None),
        } for entry in entries]

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
            self.load_entries()

        self.date_dialog.on_save = lambda *args: ok(to, *args)

    def animate_edit_card(self):
        y = self.ids.edit_card.y
        h = self.ids.edit_card.height
        Animation(y=5 if y < 5 else -h, d=0.2).start(self.ids.edit_card)

    def on_show_filters(self, _, show):
        if show:
            s = self.ids.filter_tag_box.height * self.ids.filter_tag_box.width
            h = s / self.width
            h = self.ids.filter_tag_box.height if h < self.ids.filter_tag_box.height else h
            w = s / h
            x = self.width - w
            Animation(
                width=w,
                height=h + dp(10),
                top=self.ids.filter_tag_box_container_placeholder.top,
                corner_radius=dp(20),
                x=x,
                d=0.2
            ).start(self.ids.filter_tag_box_container)

        else:
            Animation(
                size=self.ids.filter_tag_box_container_placeholder.size,
                pos=self.ids.filter_tag_box_container_placeholder.pos,
                corner_radius=0,
                d=0.2
            ).start(self.ids.filter_tag_box_container)

            self.load_entries()

        # putting the important tags close to the top
        self.ids.filter_tag_box.clear_widgets(self.re_add_tags)
        for tagc in self.re_add_tags:
            self.ids.filter_tag_box.add_widget(tagc, len(self.ids.filter_tag_box.children))
        self.re_add_tags = []

    def on_touch_down(self, touch):
        r = super(EntriesScreen, self).on_touch_down(touch)
        if self.to_local(*touch.pos)[1] > self.ids.edit_card.top + 50 and self.ids.edit_card.y >= 0:
            self.animate_edit_card()
        if self.show_filters and self.ids.filter_tag_box_container.y > self.to_local(*touch.pos)[1]:
            self.show_filters = False

        return r

    def on_entry_edit(self, _, __):
        self.on_edit_field_text(self.ids.edit_field, self.ids.edit_field.text)

    def on_edit_field_text(self, field, text):
        if (not self.entry_edit) or ("%%" not in text):
            return
        start = text.find("%%")
        if " " in text[start:]:
            end = text[start:].find(" ") + start
        elif "\n" in text[start:]:
            end = text[start:].find("\n") + start
        else:
            return

        tag = text[start:end]
        if tag[2:]:
            self.ids.tag_box.add_widget(TagChip(
                text=tag[2:],
                on_press=lambda x: x.parent.remove_widget(x)
            ))

        def remove_tag_from_text(_):
            field.text = text[:-1].replace(tag, "")

        Clock.schedule_once(remove_tag_from_text, 0)

    def add_attachment(self, files):
        for attachment in files:
            self.ids.attachment_box.add_widget(AttachmentCard(attachment=Attachment(path=attachment)))

    def save_entry(self):
        content = self.ids.edit_field.text
        tags = [tc.text for tc in self.ids.tag_box.children]
        attachments = [att.attachment.path for att in self.ids.attachment_box.children]
        if not self.editing_entry:
            Entry(tags=list(filter(bool, set(tags))), content=content, attachments=attachments).save()
        else:
            self.editing_entry.content = content
            self.editing_entry.current_tags = tags
            self.editing_entry.new_attachments(attachments)
            self.editing_entry.save()

        self.load_entries()

        self.editing_entry = None
        self.ids.edit_field.text = ""
        self.ids.tag_box.clear_widgets()
        self.ids.attachment_box.clear_widgets()

        self.animate_edit_card()

    def save_post(self):
        # print(dir(self.parent))
        content = self.ids.edit_field.text
        attachments = [att.attachment.path for att in self.ids.attachment_box.children]
        if not self.editing_post:
            Post(content=content, attachments=attachments).save()
        else:
            self.editing_post.content = content
            self.editing_post.new_attachments(attachments)
            self.editing_post.save()

        self.load_entries()

        self.editing_post = None
        self.ids.edit_field.text = ""
        self.ids.attachment_box.clear_widgets()
        self.animate_edit_card()

        posts_screen = self.parent.get_screen("posts_screen")
        posts_screen.load_posts()
        self.parent.switch_to(posts_screen)

    def edit_past_entry(self, entry):
        self.animate_edit_card()

        self.editing_entry = entry
        self.ids.edit_field.text = entry.content
        self.ids.tag_box.clear_widgets()
        self.add_tags(entry.tags)
        self.ids.attachment_box.clear_widgets()
        self.add_attachments(entry.attachments)

    def add_tags(self, tags):
        self.ids.tag_box.clear_widgets()
        for tag in tags:
            self.ids.tag_box.add_widget(TagChip(tag=tag, on_press=lambda x: x.parent.remove_widget(x)))

    def add_attachments(self, attachments):
        self.ids.attachment_box.clear_widgets()
        for attachment in attachments:
            self.ids.attachment_box.add_widget(AttachmentCard(attachment=attachment))
