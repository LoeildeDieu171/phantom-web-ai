from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="web", html=True), name="web")

class Message(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(msg: Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es Phantom AI, un assistant sombre, intelligent et calme."},
            {"role": "user", "content": msg.message}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }
