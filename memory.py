import chromadb

db = chromadb.Client()
memory = db.get_or_create_collection("phantom_memory")

def remember(user_id, text):
    memory.add(
        documents=[text],
        metadatas=[{"user": user_id}],
        ids=[str(hash(text))]
    )

def recall(user_id, query):
    r = memory.query(query_texts=[query], n_results=3)
    return " ".join(r["documents"][0]) if r["documents"] else ""
