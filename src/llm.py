from google import genai
from dotenv import load_dotenv

load_dotenv()


class DuengeonMaster:
    def __init__(self, chat_history=None):
        self.global_chat_history = chat_history
        self.client = genai.Client()
        self.chat = self.client.chats.create(model="gemini-1.5-flash")
        # self.game_start = self.chat.send_message(str(self.global_chat_history))
        # print(self.game_start.text)

    def inference(self, input_text):
        self.global_chat_history.append({"User": input_text})
        response = self.chat.send_message(str(self.global_chat_history))
        self.global_chat_history.append({"Dungeon Master": response.text})
        return response.text
