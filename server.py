from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/")
def index():
    return FileResponse("web/index.html")

@app.post("/ask")
async def ask(data: dict):
    question = data.get("question", "").strip()

    def stream():
        process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        prompt = f"""
Tu es PHANTOM AI.
Réponds naturellement, clairement.
Tu sais tout ce qu’un LLM sait.
Tu écris du code si demandé.

Question :
{question}

Réponse :
"""
        process.stdin.write(prompt)
        process.stdin.close()

        for line in process.stdout:
            yield line

    return StreamingResponse(stream(), media_type="text/plain")
