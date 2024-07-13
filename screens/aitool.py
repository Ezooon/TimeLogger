from kivy.lang import Builder
from uix.messagecard import MessageCard
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


Builder.load_file("screens/aitool.kv")


class AiToolScreen(MDBottomNavigationItem):

    def send(self, prompt_field):
        prompt = prompt_field.text
        self.add_message("You", prompt)
        # aitool.chat.send(prompt)

    def add_message(self, sender, content):
        print(content)
        msg_card = MessageCard(sender=sender, content=content)
        self.ids.messages.add_widget(msg_card)

