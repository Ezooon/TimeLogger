from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.dialog import BaseDialog
from utils import resource_path
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.lang import Builder
from kivy.loader import Loader
from kivy.clock import Clock
from kivy.app import App

Loader.loading_image = resource_path("assets/file.png")
Builder.load_file(resource_path("uix/attachmentcard.kv"))


def on_touch_down(_, touch):
    if view_img._is_open:
        view_img.dismiss()


view_img = BaseDialog(elevation=0, anchor_x="left", anchor_y='bottom')
img = AsyncImage()
path_label = MDLabel(text=resource_path("assets/file.png"), adaptive_height=True)
path_label.md_bg_color = 0, 0, 0, 0.5
path_label.font_size = '23sp'
path_label.padding = '15dp'
path_label.pos = 0, 0
view_img.add_widget(img)
view_img.add_widget(path_label)
view_img.bind(on_touch_down=on_touch_down)


class AttachmentCard(ButtonBehavior, MDFloatLayout):
    attachment = ObjectProperty()

    path = StringProperty(resource_path("assets/file.png"))

    def on_attachment(self, _, att):
        self.path = att.path

    def on_release(self):
        img.source = self.path
        path_label.text = self.path
        view_img.open()

    def delete(self):
        app = App.get_running_app()
        parent = self.parent
        self.parent.remove_widget(self)
        app.snackbar.open()

        def permanent_delete(_):
            if not app.undo:
                self.attachment.delete()
            else:
               parent.add_widget(self)
            app.undo = False

        Clock.schedule_once(permanent_delete, 5)
