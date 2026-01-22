from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI()

# CORS pour autoriser Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

GREETINGS = [
    "Salut 👋",
    "Hey !",
    "Bonjour 😄",
    "Yo.",
    "Hello."
]

THINKING = [
    "Bonne question.",
    "Voyons ça ensemble.",
    "Intéressant 🤔",
    "Je comprends.",
    "Laisse-moi réfléchir."
]

TECH = [
    "D’un point de vue technique,",
    "En développement,",
    "Si on parle de code,",
    "Côté web,",
    "Dans la pratique,"
]

CLOSING = [
    "Tu veux que je détaille ?",
    "On peut aller plus loin.",
    "Dis-moi si tu veux un exemple.",
    "Je peux t’aider davantage.",
    "À toi."
]

def generate_response(user_msg: str) -> str:
    msg = user_msg.lower()
    parts = []

    parts.append(random.choice(GREETINGS))
    parts.append(random.choice(THINKING))

    if any(w in msg for w in ["code", "script", "js", "html", "css", "python", "site"]):
        parts.append(random.choice(TECH))
        parts.append(
            "il existe plusieurs façons de faire selon ton objectif, "
            "ton niveau et ce que tu veux obtenir exactement."
        )
    elif any(w in msg for w in ["qui es", "t'es qui", "tu es quoi"]):
        parts.append(
            "je suis Phantom AI, une intelligence artificielle conçue pour "
            "répondre intelligemment et évoluer avec le temps."
        )
    elif any(w in msg for w in ["aide", "help", "problème"]):
        parts.append(
            "explique-moi précisément ce qui bloque et je ferai de mon mieux "
            "pour te guider étape par étape."
        )
    else:
        parts.append(
            "ta question est intéressante et peut être abordée de plusieurs manières."
        )

    parts.append(random.choice(CLOSING))
    return " ".join(parts)

@app.post("/chat")
def chat(data: ChatMessage):
    time.sleep(random.uniform(0.4, 1.1))  # effet humain
    return {"response": generate_response(data.message)}

@app.get("/")
def root():
    return {"status": "Phantom AI backend online"}
