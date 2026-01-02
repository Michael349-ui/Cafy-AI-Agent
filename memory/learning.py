from memory.vector_store import store

def store_correction(question, wrong, correct):
    text = f"""
USER QUESTION:
{question}

WRONG ANSWER:
{wrong}

CORRECT ANSWER:
{correct}
"""
    store(text, {"type": "correction"})
