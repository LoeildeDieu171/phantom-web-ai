import os
from config import ALLOWED_EXT

def read_project(folder):
    data = []
    for root, _, files in os.walk(folder):
        for f in files:
            if any(f.endswith(ext) for ext in ALLOWED_EXT):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()[:4000]  # limite sécurité
                        data.append(f"\n### FILE: {path}\n{content}")
                except:
                    pass
    return "\n".join(data)
