from memory.vector_store import search

def retrieve_memory(query: str, k: int = 3) -> str:
    docs = search(query, k)
    joined = "\n\n".join(docs)
    return joined[:8000]   # hard cap
