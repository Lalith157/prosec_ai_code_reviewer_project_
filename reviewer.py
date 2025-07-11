import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "codellama:7b"

def review_code_with_ollama(code):
    prompt = (
        "You are a code reviewer. Review the following Python code and provide suggestions, bugs, or improvements in short, useful bullet points.\n\n"
        f"{code}"
    )
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_URL, json=data, timeout=120)
        resp.raise_for_status()
        result = resp.json()
        return result.get("response", "").strip()
    except Exception as e:
        print(f"Ollama error: {e}")
        return None
