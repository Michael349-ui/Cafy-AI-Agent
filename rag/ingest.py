import inspect
import os
from memory.vector_store import store

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

CAFY_FILES = [
    "cafy_apis/ixia_generated.py",
    "cafy_apis/ixia_multicast.py",
]

def ingest_file(path):
    full_path = os.path.join(PROJECT_ROOT, path)

    with open(full_path, "r", encoding="utf-8") as f:
        source = f.read()

    store(
        text=source,
        metadata={
            "type": "cafy_source",
            "file": path
        }
    )

if __name__ == "__main__":
    for file in CAFY_FILES:
        ingest_file(file)

    print("CAFy API source files ingested successfully.")
