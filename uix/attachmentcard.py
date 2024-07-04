from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.lang import Builder
from kivy.loader import Loader
from kivy.clock import Clock
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton

Loader.loading_image = "assets/file.png"
Builder.load_file("uix/attachmentcard.kv")
undo = False


def set_undo_to_true(*_):
    global undo
    undo = True


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


snackbar = MDSnackbar()
snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
snackbar.add_widget(MDLabel(text="An Attachment Was Deleted!", adaptive_height=True))
snackbar.add_widget(MDSnackbarActionButton(
        text="Undo?",
        text_color=(1, 1, 1, 1),
        on_release=set_undo_to_true,
        ))


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
        parent = self.parent
        self.parent.remove_widget(self)
        snackbar.open()

        global undo
        undo = False

        def permanent_delete(_):
            if not undo:
                pass
                self.attachment.delete()
                return
            parent.add_widget(self)

        Clock.schedule_once(permanent_delete, 5)

