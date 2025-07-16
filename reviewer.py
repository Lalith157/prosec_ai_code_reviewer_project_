import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "codellama:7b"

EXTENSION_TO_LANGUAGE = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.cs': 'C#',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.rs': 'Rust',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.sh': 'Shell',
    '.pl': 'Perl',
    '.r': 'R',
    '.m': 'MATLAB',
    '.sql': 'SQL',
    '.html': 'HTML'
    '.css': 'CSS'
    '.js': 'JavaScript'
    # Add more as needed
}

def get_language_from_extension(filename):
    for ext, lang in EXTENSION_TO_LANGUAGE.items():
        if filename.endswith(ext):
            return lang
    return "code"  # fallback

def get_review_prompt(language, code):
    return (
        f"You are a strict {language} code reviewer. "
        "Review the following code and provide suggestions, bugs, or improvements in short, useful bullet points. "
        "If you find security vulnerabilities, highlight them. "
        "If the code is fine, reply ONLY with 'OK'.\n\n"
        f"{code}"
    )

def review_code_with_ollama(code, language):
    prompt = get_review_prompt(language, code)
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
