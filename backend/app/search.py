import numpy as np
from chromadb import Client
from ollama import embeddings

client = Client()
collection = client.get_or_create_collection("docs")

def chunk_text(text, size=1000):
    return [text[i:i + size] for i in range(0, len(text), size)]

def index_doc(doc_id: str, text: str):
    if not text.strip():
        return
    chunks = chunk_text(text, size=2000) 
    all_embeddings = []
    for chunk in chunks:
        try:
            res = embeddings(model="nomic-embed-text", prompt=chunk)
            all_embeddings.append(res["embedding"])
        except Exception as e:
            print(f"Error embedding chunk: {e}")

    if not all_embeddings:
        return

    final_emb = np.mean(all_embeddings, axis=0).tolist()
    collection.add(
        ids=[doc_id], 
        embeddings=[final_emb], 
        documents=[text[:5000]] 
    )

# --- ADD THIS FUNCTION BACK ---
def semantic_search(query: str):
    if not query.strip():
        return []
    
    try:
        qemb = embeddings(model="nomic-embed-text", prompt=query)["embedding"]
        res = collection.query(query_embeddings=[qemb], n_results=5)
        
        if res and res['documents']:
            return res['documents'][0]
        return []
    except Exception as e:
        print(f"Search error: {e}")
        return []