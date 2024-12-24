from typing import Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()


class DuengeonMaster:
    def __init__(self):
        self.client = genai.Client()
        self.chat = self.client.chats.create(model="gemini-1.5-flash")

        with open(
            "/home/capybara/code/ml/LLM-Role-Playing-Game/src/prompt.xml", "r"
        ) as file:
            context = file.read().replace("\n", "")
        self.global_chat_history = [{"System": context}]

    def inference(self, input_text: Optional[str | None] = None):
        if input_text is None:
            return self.chat.send_message(str(self.global_chat_history)).text

        self.global_chat_history.append({"User": input_text})
        response = self.chat.send_message(str(self.global_chat_history))
        self.global_chat_history.append({"Dungeon Master": response.text})
        return response.text
