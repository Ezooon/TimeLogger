import threading
from kivy.lang import Builder
from uix.messagecard import MessageCard
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.clock import mainthread
from aitool import chat


Builder.load_file("screens/aitool.kv")


class AiToolScreen(MDBottomNavigationItem):

    def send(self, prompt_field):
        prompt = prompt_field.text

        entries_screen = self.parent.get_screen("entries_screen")
        entries = [entry_card["entry"] for entry_card in entries_screen.view_data]

        self.add_message("User", prompt)

        successes = lambda x: self.add_message("BOT", x)
        threading.Thread(target=chat.send, args=(entries, prompt, self.get_history(), successes, successes)).start()

    def get_history(self):
        history = []
        for msg_card in self.ids.messages.children:
            history.append(f"{msg_card.sender}: {msg_card.content}")
        return history

    @mainthread
    def add_message(self, sender, content):
        msg_card = MessageCard(sender=sender, content=str(content))
        self.ids.messages.add_widget(msg_card)
        return msg_card

