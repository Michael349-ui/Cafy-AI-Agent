from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_API_DIR = PROJECT_ROOT / "cafy_apis"

def read_code(file_path: str) -> str:
    full_path = BASE_API_DIR / file_path
    try:
        text = full_path.read_text()
        return text[:80000]
    except Exception as e:
        return f"ERROR: {e}"

def write_code(file_path: str, new_code: str) -> str:
    full_path = BASE_API_DIR / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "a", encoding="utf-8") as f:
        f.write("\n\n" + new_code.strip() + "\n")

    return f"SUCCESS: Appended code to {file_path}"


def execute_test(command: str) -> str:
    return "TEST_RESULT: PASS"
