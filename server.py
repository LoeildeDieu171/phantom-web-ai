# ===============================
# PHANTOM AI - BACKEND STABLE
# ===============================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import traceback
import datetime
import os
import json

# ===============================
# APP INIT
# ===============================

app = FastAPI(title="Phantom AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# LOG SYSTEM
# ===============================

LOG_FILE = "logs.txt"

def log(msg: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

log("Server booting")

# ===============================
# CONFIG
# ===============================

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

# ===============================
# STATIC FILES
# ===============================

if not os.path.isdir("web"):
    log("ERROR: web/ directory missing")

app.mount("/", StaticFiles(directory="web", html=True), name="web")

# ===============================
# HEALTH CHECK
# ===============================

@app.get("/api/health")
def health():
    return {
        "ok": True,
        "openai_key_loaded": bool(OPENAI_KEY),
        "time": datetime.datetime.now().isoformat()
    }

# ===============================
# SAFE JSON PARSE
# ===============================

async def safe_json(req: Request):
    try:
        return await req.json()
    except Exception as e:
        log(f"JSON parse error: {e}")
        return {}

# ===============================
# CHAT ENDPOINT
# ===============================

@app.post("/api/chat")
async def chat(req: Request):
    try:
        data = await safe_json(req)
        user_message = str(data.get("message", "")).strip()

        log(f"User message: {user_message}")

        if not user_message:
            return JSONResponse(
                status_code=200,
                content={"reply": "Tu n’as rien écrit."}
            )

        # ===============================
        # MODE SANS OPENAI
        # ===============================
        if not OPENAI_KEY:
            log("No OpenAI key -> local fallback")
            return JSONResponse(
                status_code=200,
                content={
                    "reply": (
                        "⚠ MODE LOCAL ACTIVÉ\n\n"
                        f"Tu as écrit : {user_message}\n\n"
                        "Ajoute une clé OpenAI pour activer l’IA réelle."
                    )
                }
            )

        # ===============================
        # OPENAI REQUEST
        # ===============================
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Tu es Phantom AI, calme, précis, sombre."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        }

        log("Sending request to OpenAI")

        response = requests.post(
            OPENAI_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        log(f"OpenAI status: {response.status_code}")

        if response.status_code != 200:
            log(f"OpenAI error body: {response.text}")
            return JSONResponse(
                status_code=200,
                content={
                    "reply": (
                        "Erreur OpenAI.\n\n"
                        f"Code: {response.status_code}\n"
                        f"Détail: {response.text[:500]}"
                    )
                }
            )

        data = response.json()

        try:
            reply = data["choices"][0]["message"]["content"]
        except Exception:
            log("Malformed OpenAI response")
            return JSONResponse(
                status_code=200,
                content={"reply": "Réponse OpenAI invalide."}
            )

        return JSONResponse(status_code=200, content={"reply": reply})

    except Exception as e:
        tb = traceback.format_exc()
        log(f"FATAL ERROR: {e}\n{tb}")
        return JSONResponse(
            status_code=200,
            content={
                "reply": (
                    "Erreur interne contrôlée.\n\n"
                    f"{str(e)}"
                )
            }
        )
