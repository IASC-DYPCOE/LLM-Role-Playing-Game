from google import genai
from dotenv import load_dotenv

load_dotenv()

context = """"""
global_chat_history = {}

client = genai.Client()
chat = client.chats.create(model="gemini-1.5-flash")
response = chat.send_message("tell me a story")
print(response.text)
