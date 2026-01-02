# config.py

# ---------------------------
# Embeddings
# ---------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # local, fast, reliable

# ---------------------------
# FAISS storage
# ---------------------------
DATA_DIR = "data"
FAISS_INDEX_PATH = "data/cafy.index"
FAISS_META_PATH = "data/cafy_meta.json"

# ---------------------------
# RAG behavior
# ---------------------------
TOP_K_RETRIEVAL = 2
