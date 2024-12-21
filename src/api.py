from .utils import extract_json
from fastapi import FastAPI, Request, Response, Form
from .llm import DuengeonMaster

app = FastAPI()

duengeon_master = DuengeonMaster()


@app.get("/dnd/start")
async def start(request: Request, Response: Response):
    with open(
        "/home/capybara/code/ml/LLM-Role-Playing-Game/src/prompt.xml", "r"
    ) as file:
        context = file.read().replace("\n", "")
    global_chat_history = [{"System": context}]
    duengeon_master.set_global_chat_history(global_chat_history)
    return {"content": "New game started!"}


@app.post("/dnd/play")
async def home(request: Request, Response: Response, form_input_text: str = Form()):
    input_text = form_input_text
    print(input_text)
    response = duengeon_master.inference(input_text)
    response = extract_json(response)
    return response
