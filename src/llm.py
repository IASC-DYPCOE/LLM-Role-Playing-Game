from typing import Optional, List, Dict
from google import genai
from dotenv import load_dotenv

load_dotenv()


class DungeonMaster:
    def __init__(self):
        self.client = genai.Client()
        self.chat = self.client.chats.create(model="gemini-1.5-flash")
        with open(
            "/home/capybara/code/ml/LLM-Role-Playing-Game/src/prompt.xml", "r"
        ) as file:
            self.context = file.read().replace("\n", "")

    def format_history(self, chat_history: List[Dict[str, str]]) -> str:
        """Format chat history into a single string for the LLM."""
        formatted_messages = []
        formatted_messages.append(self.context)

        for message in chat_history:
            role = message["role"]
            content = message["content"]
            if role == "user":
                formatted_messages.append(f"Player: {content}")
            else:
                formatted_messages.append(f"Dungeon Master: {content}")

        return " ".join(formatted_messages)

    def inference(
        self, chat_history: List[Dict[str, str]], new_message: Optional[str] = None
    ) -> str:
        if new_message:
            temp_history = chat_history + [{"role": "user", "content": new_message}]
            full_context = self.format_history(temp_history)
        else:
            full_context = self.format_history(chat_history)

        response = self.chat.send_message(full_context).text
        return response
