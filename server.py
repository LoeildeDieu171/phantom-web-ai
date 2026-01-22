from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

GREETINGS = [
    "Salut !", "Hey 👋", "Bonjour 😄", "Yo !", "Hello."
]

THINKING = [
    "Bonne question.",
    "Voyons ça ensemble.",
    "Intéressant 🤔",
    "Je vois ce que tu veux dire.",
    "Laisse-moi réfléchir."
]

ANSWERS_GENERAL = [
    "Voici ce que je peux te dire.",
    "Voilà une réponse possible.",
    "D’après mes connaissances.",
    "Voici une explication claire.",
    "Je vais t’expliquer simplement."
]

TECH = [
    "En programmation,",
    "D’un point de vue technique,",
    "Si on parle de code,",
    "Dans le développement web,",
    "Côté logiciel,"
]

CLOSING = [
    "Si tu veux, je peux aller plus loin.",
    "Dis-moi si tu veux un exemple.",
    "Tu veux que je détaille ?",
    "On peut approfondir.",
    "À toi de me dire."
]

def generate_response(user_message: str) -> str:
    msg = user_message.lower()

    parts = []

    parts.append(random.choice(GREETINGS))
    parts.append(random.choice(THINKING))

    if any(word in msg for word in ["code", "script", "js", "python", "site"]):
        parts.append(random.choice(TECH))
        parts.append(random.choice(ANSWERS_GENERAL))
        parts.append(
            "il existe plusieurs manières de résoudre ton problème, "
            "selon ce que tu veux exactement obtenir."
        )
    elif any(word in msg for word in ["qui es-tu", "t'es qui", "tu es quoi"]):
        parts.append(
            "je suis Phantom AI, une intelligence artificielle conçue pour "
            "répondre intelligemment et évoluer avec le temps."
        )
    elif any(word in msg for word in ["aide", "help", "problème"]):
        parts.append(
            "explique-moi précisément ce qui ne fonctionne pas, "
            "et je ferai de mon mieux pour t’aider."
        )
    else:
        parts.append(
            "ta question est intéressante et peut être abordée de plusieurs façons."
        )

    parts.append(random.choice(CLOSING))

    return " ".join(parts)

@app.post("/chat")
def chat(data: Message):
    time.sleep(random.uniform(0.4, 1.2))  # effet humain
    return {"response": generate_response(data.message)}
