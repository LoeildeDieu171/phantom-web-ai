from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()

# AUTORISE LE FRONT À PARLER AU BACKEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

RESPONSES = [
    "Ça va plutôt bien 😄 Et toi ?",
    "Oui, tranquille. Qu’est-ce que tu veux faire ?",
    "Toujours opérationnel 💪",
    "Je suis là. Dis-moi.",
    "Tout roule. Tu veux parler de quoi ?"
]

@app.post("/chat")
async def chat(data: Message):
    return {
        "response": random.choice(RESPONSES)
    }

# ⚠️ IMPORTANT : lancer le serveur
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
