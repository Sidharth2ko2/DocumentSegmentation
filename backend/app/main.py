from fastapi import FastAPI, UploadFile, File  # Added File
from fastapi.middleware.cors import CORSMiddleware
from typing import List  # Added List
from app.ingest import read_file, save_doc
from app.search import index_doc, semantic_search
from app.classifier.infer import classify
from app.db import cur  # Added cur for history to work

app = FastAPI()

# Allow your React app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/upload')
async def upload(files: List[UploadFile] = File(...)): 
    results = []
    # We only process the first 10 files
    for file in files[:10]:
        text = await read_file(file)
        label, conf = classify(text)
        save_doc(file.filename, text, label, conf)
        index_doc(file.filename, text)
        results.append({
            'name': file.filename,
            'label': label, 
            'confidence': conf
        })
    return results

@app.get('/search')
async def search(q: str = ""):
    if not q.strip():
        return {'results': []}
    return {'results': semantic_search(q)}

@app.get('/history')
async def get_history():
    # Fetching the last 10 classified documents
    cur.execute("SELECT name, label, confidence FROM documents ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    return [{"name": r[0], "label": r[1], "confidence": r[2]} for r in rows]