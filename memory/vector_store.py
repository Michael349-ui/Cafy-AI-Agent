import os
import json
import uuid
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
    FAISS_META_PATH
)

# ---------------------------
# Ensure data directory exists
# ---------------------------
os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)

# ---------------------------
# Load embedding model
# ---------------------------
embedder = SentenceTransformer(EMBEDDING_MODEL)
DIM = embedder.get_sentence_embedding_dimension()

# ---------------------------
# Load / Init FAISS index
# ---------------------------
try:
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
    else:
        raise RuntimeError("Index not found")
except Exception:
    index = faiss.IndexFlatL2(DIM)


# ---------------------------
# Load / Init metadata
# ---------------------------
if os.path.exists(FAISS_META_PATH):
    with open(FAISS_META_PATH, "r", encoding="utf-8") as f:
        metadata_store = json.load(f)
else:
    metadata_store = []

# ---------------------------
# Internal helpers
# ---------------------------
def _save():
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(FAISS_META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata_store, f, indent=2)

def _embed(texts):
    return embedder.encode(
        texts,
        normalize_embeddings=True
    ).astype("float32")

# ---------------------------
# Public API
# ---------------------------
def store(text: str, metadata: dict):
    emb = _embed([text])
    index.add(emb)

    metadata_store.append({
        "id": str(uuid.uuid4()),
        "text": text,
        "metadata": metadata
    })

    _save()

def search(query: str, k: int = 5):
    if index.ntotal == 0:
        return []

    q_emb = _embed([query])
    _, idxs = index.search(q_emb, k)

    return [
        metadata_store[i]["text"]
        for i in idxs[0]
        if i < len(metadata_store)
    ]
