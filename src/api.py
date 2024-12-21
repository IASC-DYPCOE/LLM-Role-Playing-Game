from fastapi import FastAPI, Request, Response
from llm import DuengeonMaster

app = FastAPI()

context = ""
with open("./prompt.xml", "r") as file:
    context += file.read().replace("\n", "")
global_chat_history = [{"System": context}]
duengeon_master = DuengeonMaster(global_chat_history)


@app.get("/")
def home(request, Request: Request, Response: Response):
    input_text = request.query_params.get("input_text")
    response = duengeon_master.inference(input_text)
    return {"response": response}
