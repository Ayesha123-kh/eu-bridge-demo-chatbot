import logging
import os

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel

from services.analytics import track_search
from services.screening import rank_candidates

logger = logging.getLogger("hirebot")
logging.basicConfig(level=logging.INFO)

app = FastAPI()
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

app.mount("/static", StaticFiles(directory="static"), name="static")

PORT = int(os.environ.get("PORT", "8000"))


class ChatRequest(BaseModel):
    email: str
    phone: str
    message: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/chat")
def chat(req: ChatRequest):
    print(f"User {req.email} said: {req.message}")
    track_search(req.email, req.message)
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are HireBot, an assistant that answers applicants' questions about open roles."},
            {"role": "user", "content": req.message},
        ],
    )
    return {"reply": completion.choices[0].message.content}


@app.post("/upload-cv")
async def upload_cv(applicant_name: str = Form(...), applicant_phone: str = Form(...), cv: UploadFile = File(...)):
    text = (await cv.read()).decode("utf-8", errors="ignore")
    logger.info("CV received from %s, phone %s", applicant_name, applicant_phone)
    summary = anthropic_client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=400,
        messages=[{"role": "user", "content": f"Summarise this CV for a recruiter:\n{text}"}],
    )
    score = rank_candidates(text)
    return {"summary": summary.content[0].text, "score": score}


@app.on_event("startup")
def started():
    logger.info("HireBot started on port %s", PORT)


@app.exception_handler(Exception)
async def on_error(request, exc):
    logger.error("Unhandled error: %s", exc)
    return {"error": "Something went wrong"}
