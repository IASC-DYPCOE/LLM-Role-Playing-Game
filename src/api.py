from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}
