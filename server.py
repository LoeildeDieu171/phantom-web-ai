# ============================================================
# PHANTOM AI - SERVER BACKEND
# Author: ChatGPT (for Phantom Project)
# Purpose: Stable AI backend with zero-crash philosophy
# ============================================================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import traceback
import datetime
import json
import os
import sys
import threading
import time
from typing import Dict, Any, Optional

# ============================================================
# GLOBAL CONSTANTS
# ============================================================

APP_NAME = "Phantom AI"
APP_VERSION = "1.0.0"
LOG_FILE = "server.log"
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-3.5-turbo"
REQUEST_TIMEOUT = 30

# ============================================================
# SAFE LOGGING SYSTEM
# ============================================================

_log_lock = threading.Lock()

def log(message: str, level: str = "INFO") -> None:
    """
    Thread-safe logger.
    Writes to console and file.
    """
    with _log_lock:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"
        print(line)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            # Logging must NEVER crash the server
            pass

log("Starting Phantom AI backend")

# ============================================================
# ENVIRONMENT & CONFIG
# ============================================================

def load_env_key() -> str:
    """
    Loads OpenAI key safely.
    Never throws.
    """
    try:
        return os.getenv("OPENAI_API_KEY", "").strip()
    except Exception:
        return ""

OPENAI_KEY = load_env_key()

def openai_enabled() -> bool:
    return bool(OPENAI_KEY)

log(f"OpenAI key loaded: {openai_enabled()}")

# ============================================================
# FASTAPI INITIALIZATION
# ============================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# STATIC FILE SERVING
# ============================================================

WEB_DIR = "web"

if os.path.isdir(WEB_DIR):
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
    log("Static web directory mounted")
else:
    log("WARNING: web/ directory not found", "WARN")

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

async def safe_json(request: Request) -> Dict[str, Any]:
    """
    Safely parse JSON body.
    Never raises.
    """
    try:
        return await request.json()
    except Exception as e:
        log(f"JSON parse error: {e}", "WARN")
        return {}

def safe_str(value: Any) -> str:
    """
    Convert anything to string safely.
    """
    try:
        return str(value)
    except Exception:
        return ""

def truncate(text: str, limit: int = 5000) -> str:
    """
    Prevent extremely large payloads.
    """
    if len(text) > limit:
        return text[:limit]
    return text

# ============================================================
# HEALTH & DEBUG ENDPOINTS
# ============================================================

@app.get("/api/health")
def health_check():
    """
    Health endpoint used for monitoring.
    """
    return {
        "ok": True,
        "name": APP_NAME,
        "version": APP_VERSION,
        "openai_enabled": openai_enabled(),
        "time": datetime.datetime.utcnow().isoformat()
    }

@app.get("/api/debug/env")
def debug_env():
    """
    Debug endpoint (no secrets exposed).
    """
    return {
        "python": sys.version,
        "cwd": os.getcwd(),
        "openai_key_loaded": openai_enabled(),
        "web_dir_exists": os.path.isdir(WEB_DIR)
    }

# ============================================================
# CORE AI LOGIC
# ============================================================

def call_openai(user_message: str) -> str:
    """
    Call OpenAI API.
    Returns reply or error message.
    NEVER raises.
    """
    try:
        payload = {
            "model": DEFAULT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Phantom AI. "
                        "You are calm, precise, intelligent, and respectful."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        }

        log("Sending request to OpenAI")

        response = requests.post(
            OPENAI_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

        log(f"OpenAI HTTP status: {response.status_code}")

        if response.status_code != 200:
            return (
                "OpenAI API error.\n\n"
                f"Status: {response.status_code}\n"
                f"Response: {truncate(response.text, 300)}"
            )

        data = response.json()

        if not isinstance(data, dict):
            return "Invalid OpenAI response format."

        choices = data.get("choices")
        if not choices or not isinstance(choices, list):
            return "OpenAI response missing choices."

        message = choices[0].get("message", {})
        content = message.get("content")

        if not content:
            return "OpenAI returned empty content."

        return content

    except requests.Timeout:
        log("OpenAI request timeout", "WARN")
        return "OpenAI request timed out. Try again."

    except Exception as e:
        log(f"OpenAI call failed: {e}", "ERROR")
        return f"OpenAI internal error: {str(e)}"

# ============================================================
# CHAT ENDPOINT (MAIN)
# ============================================================

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """
    Main chat endpoint.
    GUARANTEED to return JSON.
    """
    try:
        body = await safe_json(request)
        raw_message = body.get("message", "")
        user_message = truncate(safe_str(raw_message).strip(), 4000)

        log(f"Incoming message: {user_message}")

        if not user_message:
            return JSONResponse(
                status_code=200,
                content={"reply": "Tu dois écrire un message."}
            )

        # ----------------------------------------------------
        # FALLBACK MODE (NO OPENAI)
        # ----------------------------------------------------
        if not openai_enabled():
            log("OpenAI disabled, using fallback mode", "WARN")
            return JSONResponse(
                status_code=200,
                content={
                    "reply": (
                        "⚠ MODE LOCAL (sans OpenAI)\n\n"
                        f"Message reçu :\n{user_message}\n\n"
                        "Ajoute une clé OpenAI pour activer l’IA réelle."
                    )
                }
            )

        # ----------------------------------------------------
        # REAL AI RESPONSE
        # ----------------------------------------------------
        reply = call_openai(user_message)

        return JSONResponse(
            status_code=200,
            content={"reply": reply}
        )

    except Exception as e:
        # ABSOLUTE SAFETY NET
        tb = traceback.format_exc()
        log(f"UNHANDLED ERROR: {e}\n{tb}", "FATAL")

        return JSONResponse(
            status_code=200,
            content={
                "reply": (
                    "Erreur interne contrôlée.\n\n"
                    f"Détail: {str(e)}"
                )
            }
        )

# ============================================================
# SERVER START MESSAGE
# ============================================================

log("Phantom AI backend ready")

# End of server.py
