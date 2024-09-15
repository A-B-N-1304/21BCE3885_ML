import time
from fastapi import FastAPI, Request, HTTPException, Body
from pydantic import BaseModel
from database import get_db, create_user_if_not_exists, increment_user_request_count
from logger import log_inference_time
from config import CACHE_EXPIRY_TIME, MAX_REQUESTS
import redis
from sentence_transformers import SentenceTransformer, util
from sqlalchemy.orm import Session

app = FastAPI()

cache = redis.Redis(host='localhost', port=6379, db=0)

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

documents = []

class Document(BaseModel):
    id: int
    text: str

@app.get("/health")
async def health():
    return {"status": "Chat DRS is active and healthy!"}

@app.post("/add_document")
async def add_document(document: Document):
    global documents
    if any(doc['id'] == document.id for doc in documents):
        raise HTTPException(status_code=400, detail="Document with this ID already exists")
    
    documents.append(document.dict())
    return {"message": "Document added successfully"}

@app.post("/search")
async def search(request: Request, text: str, top_k: int = 3, threshold: float = 0.5, user_id: str = None):
    start_time = time.time()

    db: Session = next(get_db())
    create_user_if_not_exists(db, user_id)
    user_request_count = increment_user_request_count(db, user_id)

    if user_request_count > MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cache_key = f"{user_id}:{text}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return {"results": eval(cached_result)}  

    query_embedding = model.encode(text, convert_to_tensor=True)
    document_embeddings = model.encode([doc['text'] for doc in documents], convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]
    results = []
    for idx, score in enumerate(similarities):
        if score >= threshold:
            results.append({"document": documents[idx], "score": float(score)})

    results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

    cache.setex(cache_key, CACHE_EXPIRY_TIME, str(results))

    inference_time = time.time() - start_time
    log_inference_time(user_id, inference_time)

    return {"results": results, "inference_time": inference_time}
