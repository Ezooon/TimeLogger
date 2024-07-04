from kivy.lang import Builder
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty, ColorProperty


Builder.load_file("uix/tagchip.kv")


class TagChip(RectangularRippleBehavior, ButtonBehavior, MDLabel):
    # ToDo Add touch behavior and have long presses delete tags form db
    tag = ObjectProperty()

    tag_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag_color = kwargs.get("tag_color", self.theme_cls.primary_color)
        self.font_size = '15sp'

    def on_press(self):
        pass

    def on_tag(self, _, tag):
        self.text = tag.tag
