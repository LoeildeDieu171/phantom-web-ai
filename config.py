@app.post("/ask")
async def ask(data: dict):
    question = data.get("question", "").strip()
    if not question:
        return {"answer": "Écris quelque chose."}

    prompt = f"""
Tu es PHANTOM AI, une intelligence générale.
Tu réponds à TOUTES les questions du mieux possible.

Règles absolues :
- Réponds comme un humain, naturellement.
- Sois direct, clair et utile.
- Si tu sais → réponds.
- Si tu ne sais pas → dis-le honnêtement.
- N'invente PAS de faits.
- Pas de ton scolaire ou robotique.
- Pas d'excuses inutiles.

Question :
{question}

Réponse :
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return {"answer": result.stdout.strip()}
