import json, subprocess
from config import MODEL_NAME, MEMORY_FILE, SYSTEM_PROMPT
from reader import read_project

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"history": []}

def save_memory(mem):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2, ensure_ascii=False)

def ask_ai(question, context=""):
    mem = load_memory()

    prompt = SYSTEM_PROMPT + "\n\n"
    if context:
        prompt += "CONTEXTE PROJET:\n" + context + "\n\n"

    for h in mem["history"][-3:]:
        prompt += f"User: {h['q']}\nAI: {h['a']}\n"

    prompt += f"User: {question}\nAI:"

    r = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        text=True,
        capture_output=True
    )

    answer = r.stdout.strip()
    mem["history"].append({"q": question, "a": answer})
    save_memory(mem)
    return answer

if __name__ == "__main__":
    print("📂 Mode analyse de projet activé")
    folder = input("Chemin du dossier à analyser : ").strip()
    project_context = read_project(folder)

    print("✅ Projet chargé. Pose tes questions.\n")

    while True:
        q = input(">>> ")
        if q.lower() == "exit":
            break
        print("\n" + ask_ai(q, project_context) + "\n")
