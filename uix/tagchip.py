from kivy.app import App
from utils import resource_path
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, ColorProperty
from kivymd.uix.behaviors import RectangularRippleBehavior

Builder.load_file(resource_path("uix/tagchip.kv"))


class TagChip(RectangularRippleBehavior, ButtonBehavior, MDLabel):
    dialog = None

    edit_tag = None

    tag = ObjectProperty()

    tag_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag_color = kwargs.get("tag_color", self.theme_cls.primary_color)
        self.font_size = '15sp'
        if not TagChip.dialog:
            field = MDTextField()
            dialog = MDDialog(
                title="Edit or Delete Tag",
                type="custom",
                content_cls=field,
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.text_color,
                        on_press=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Delete",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.error_color,
                        on_press=lambda x: TagChip.delete_tag()
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda x: TagChip.save_tag()
                    ),
                ],
            )
            TagChip.dialog = dialog

    @classmethod
    def save_tag(cls):
        cls.edit_tag.tag = cls.dialog.content_cls.text
        cls.edit_tag.save()
        cls.dialog.dismiss()
        sc = App.get_running_app().root.ids.entries_screen
        sc.load_tags()
        sc.load_entries()

    @classmethod
    def delete_tag(cls):
        cls.edit_tag.delete()
        cls.dialog.dismiss()
        sc = App.get_running_app().root.ids.entries_screen
        sc.load_tags()
        sc.load_entries()

    def on_press(self):
        def held(_):
            if self.state == "down":
                self.on_held()

        Clock.schedule_once(held, 0.5)

    def on_release(self):
        pass

    def on_held(self, *args):
        print(self)
        TagChip.edit_tag = self.tag
        TagChip.dialog.content_cls.text = self.tag.tag
        TagChip.dialog.open()

    def on_tag(self, _, tag):
        self.text = tag.tag
