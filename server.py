from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()

# CORS (OPEN)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SERVE FRONTEND
app.mount("/", StaticFiles(directory="web", html=True), name="web")

# ========= CONFIG =========
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# ========= API CHAT =========
@app.post("/api/chat")
async def chat(req: Request):
    try:
        data = await req.json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return JSONResponse(
                status_code=200,
                content={"reply": "Écris quelque chose pour que je puisse répondre."}
            )

        # 🔥 FALLBACK SI PAS DE CLÉ
        if not OPENAI_KEY:
            return JSONResponse(
                status_code=200,
                content={
                    "reply": f"(MODE LOCAL)\nTu as dit : {user_message}\n\nAjoute une clé OpenAI pour activer l’IA réelle."
                }
            )

        # 🔥 APPEL API OPENAI (STABLE)
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es Phantom AI, une IA sombre, calme, précise."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        if r.status_code != 200:
            return JSONResponse(
                status_code=200,
                content={
                    "reply": f"Erreur OpenAI ({r.status_code}) : {r.text}"
                }
            )

        result = r.json()
        reply = result["choices"][0]["message"]["content"]

        return JSONResponse(status_code=200, content={"reply": reply})

    except Exception as e:
        # 🔥 IMPOSSIBLE D’AVOIR “Erreur serveur” SANS MESSAGE
        return JSONResponse(
            status_code=200,
            content={"reply": f"Erreur interne : {str(e)}"}
        )
