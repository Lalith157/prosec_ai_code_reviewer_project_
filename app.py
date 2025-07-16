import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from github_auth import get_installation_token
from reviewer import review_code_with_ollama
import requests
from reviewer import get_language_from_extension, get_review_prompt

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

GITHUB_APP_ID = os.getenv("1558817")
WEBHOOK_SECRET = os.getenv("changeme")

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.headers.get('X-GitHub-Event', '')
    payload = request.get_json()

    if event == "push":
        installation_id = payload["installation"]["id"]
        repo = payload["repository"]["full_name"]
        latest_commit = payload["after"]
        modified_files = set()
        for commit in payload["commits"]:
            if commit["id"] == latest_commit:
                modified_files.update(commit.get("added", []))
                modified_files.update(commit.get("modified", []))
        code_files = [f for f in modified_files if any(f.endswith(ext) for ext in EXTENSION_TO_LANGUAGE.keys())]
        if not code_files:
            logging.info("No Python files to review.")
            return jsonify({"status": "no .py files"}), 200

        token = get_installation_token(installation_id)
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

        for file_path in code_files:
            language = get_language_from_extension(file_path)
            # Fetch file content
            url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={latest_commit}"
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                logging.warning(f"Failed to fetch {file_path}: {resp.text}")
                continue
            content = resp.json().get("content", "")
            import base64
            try:
                code = base64.b64decode(content).decode("utf-8")
            except Exception as e:
                logging.warning(f"Failed to decode {file_path}: {e}")
                continue

            # Review code with Ollama
            review = review_code_with_ollama(code)
            if not review:
                logging.warning(f"No review generated for {file_path}")
                continue

            # Post commit comment
            comment_url = f"https://api.github.com/repos/{repo}/commits/{latest_commit}/comments"
            comment_body = {
                "body": f"**AI Review for `{file_path}`:**\n\n{review}"
            }
            resp = requests.post(comment_url, headers=headers, json=comment_body)
            if resp.status_code == 201:
                logging.info(f"Posted review for {file_path}")
            else:
                logging.warning(f"Failed to post comment for {file_path}: {resp.text}")

        return jsonify({"status": "reviewed"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
