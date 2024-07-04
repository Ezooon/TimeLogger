from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.lang import Builder
from kivy.loader import Loader

Loader.loading_image = "assets/file.png"
Builder.load_file("uix/attachmentcard.kv")


def on_touch_down(_, touch):
    if view_img._is_open:
        view_img.dismiss()


view_img = BaseDialog(elevation=0, anchor_x="left", anchor_y='bottom')
img = AsyncImage()
path_label = MDLabel(text="assets/file.png", adaptive_height=True)
path_label.md_bg_color = 0, 0, 0, 0.5
path_label.font_size = '23sp'
path_label.padding = '15dp'
path_label.pos = 0, 0
view_img.add_widget(img)
view_img.add_widget(path_label)
view_img.bind(on_touch_down=on_touch_down)


class AttachmentCard(ButtonBehavior, MDFloatLayout):
    attachment = ObjectProperty()

    path = StringProperty("assets/file.png")

    def on_attachment(self, _, att):
        self.path = att.path

    def on_release(self):
        img.source = self.path
        path_label.text = self.path
        view_img.open()

    def delete(self):
        self.parent.remove_widget(self)
        # self.attachment.delete()
