from utils import extract_json
from fastapi import FastAPI, Request, Response
from llm import DuengeonMaster

app = FastAPI()

context = ""
with open("./prompt.xml", "r") as file:
    context += file.read().replace("\n", "")
global_chat_history = [{"System": context}]
duengeon_master = DuengeonMaster(global_chat_history)


@app.get("/dnd")
def home(request: Request, Response: Response):
    input_text = request.form["input_text"]
    response = duengeon_master.inference(input_text)
    # response = extract_json(response)
    return response
