import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    email: str
    message: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/chat")
def chat(req: ChatRequest):
    print(f"User {req.email} said: {req.message}")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful HR assistant that screens CVs."},
            {"role": "user", "content": req.message},
        ],
    )
    return {"reply": completion.choices[0].message.content}
