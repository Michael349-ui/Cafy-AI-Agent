# memory/feedback.py
from memory.vector_store import store

def store_correction(question, wrong, correct):
    text = f"""
QUESTION:
{question}

WRONG ANSWER:
{wrong}

CORRECT ANSWER:
{correct}
"""
    store(
        text=text,
        metadata={"type": "correction"}
    )
