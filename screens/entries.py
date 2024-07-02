from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


Builder.load_file("screens/entries.kv")


class EntriesScreen(MDBottomNavigationItem):
    view_data = ListProperty([])

    def animate_edit_card(self):
        y = self.ids.edit_card.y
        print(y)
        h = self.ids.edit_card.height
        Animation(y=5 if y < 0 else -h, d=0.2).start(self.ids.edit_card)

    def on_touch_down(self, touch):
        r = super(EntriesScreen, self).on_touch_down(touch)
        if self.to_local(*touch.pos)[1] > self.ids.edit_card.top + 50 and self.ids.edit_card.y > 0:
            self.animate_edit_card()
        return r
