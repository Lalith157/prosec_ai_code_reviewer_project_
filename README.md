Certainly! Here’s a complete, clear, and user-friendly `README.md` for `AI_code_reviewer` project:

---

# AI GitHub Code Reviewer

A Python Flask GitHub App that performs **automatic AI-based code review** on every push, using a local [Ollama](https://ollama.com/) model (such as `codellama:7b`).  
The app listens for GitHub push events, fetches changed Python files, reviews them with AI, and posts the review as a commit comment.

---

## Features

- Listens to GitHub `push` events via webhook.
- Authenticates as a GitHub App using JWT.
- Extracts added/modified `.py` files from the latest commit.
- Fetches file contents and reviews them with a local Ollama model.
- Posts AI-generated review comments as commit comments on GitHub.

---

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd aigithubreviewer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Register a GitHub App

- Go to **GitHub > Settings > Developer settings > GitHub Apps > New GitHub App**.
- Set the webhook URL to:  
  `http://<your-server>:5000/webhook`
- Enable the **push** event.
- Permissions required:
  - **Contents**: Read-only
  - **Commit statuses**: Read & write
- Generate and download a private key for your app.
- Install the app on your repository.

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
GITHUB_APP_ID=your_github_app_id
GITHUB_PRIVATE_KEY_PATH=path/to/your/private-key.pem
WEBHOOK_SECRET=your_webhook_secret
```

> **Note:**  
> You do **not** need to set the installation ID; it is handled dynamically.

### 5. Run Ollama

Make sure you have [Ollama](https://ollama.com/) installed and running locally with your chosen model (e.g., `codellama:7b`):

```bash
ollama serve
ollama pull codellama:7b
```

### 6. Start the Flask Server

```bash
python app.py
```

---

## How It Works

- On every push, the app reviews new/modified Python files and posts AI feedback as commit comments.
- You can view the AI review by:
  1. Going to your repository on GitHub.
  2. Clicking on the **"Commits"** tab.
  3. Selecting the latest commit.
  4. Scrolling to the **"Comments on commit"** section.

---

## Troubleshooting

- **No review comment appears:**  
  - Ensure your Flask app is running and accessible from GitHub (use [ngrok](https://ngrok.com/) if running locally).
  - Check your Flask app logs for errors.
  - Make sure Ollama is running and the model is loaded.
- **Ollama timeout or 500 error:**  
  - Try with a smaller Python file.
  - Make sure your system has enough RAM for the model.
  - Check Ollama logs for details.

---

## Project Structure

```
aigithubreviewer/
├── app.py
├── github_auth.py
├── reviewer.py
├── requirements.txt
├── .env.example
├── README.md
```

---

## License

MIT License

---

**Enjoy automatic AI code reviews!**

If you have questions or need help, feel free to open an issue or discussion.

---

Let me know if you want any customizations or additional sections!
