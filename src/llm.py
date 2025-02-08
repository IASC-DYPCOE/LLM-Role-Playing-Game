from typing import Optional, List, Dict
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY")


class DungeonMaster:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        with open(r"prompt.xml", "r", encoding="utf-8") as file:
            self.context = file.read().replace("\n", "")

    def format_history(self, chat_history: List[Dict[str, str]]) -> str:
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

        # Add explicit instruction for response format
        full_context += " Please end your response with [Lives remaining: X] where X is the number of lives/turns the player has left."

        response = self.chat.send_message(full_context).text
        
        # Ensure response has lives remaining info
        if "[Lives remaining:" not in response:
            response += "\n[Lives remaining: 3]"  # Default value if not specified
        
        return response
