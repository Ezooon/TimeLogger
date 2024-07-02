from kivy.lang import Builder
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip


Builder.load_file("uix/tagchip.kv")


class TagChip(RectangularRippleBehavior, ButtonBehavior, MDLabel):
    def on_press(self):
        print(self.text)

