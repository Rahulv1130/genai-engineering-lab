import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# ── Google Drive ────────────────────────────────────────────────────────────
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", str(BASE_DIR / "credentials.json"))
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", str(BASE_DIR / "token.json"))

# The Drive folder ID you want to watch.
# Get it from the folder's URL: drive.google.com/drive/folders/<FOLDER_ID>
WATCHED_FOLDER_ID = os.getenv("WATCHED_FOLDER_ID", "YOUR_FOLDER_ID_HERE")

# ── Webhook ─────────────────────────────────────────────────────────────────
# Your public-facing URL (ngrok URL when running locally)
# e.g. https://abc123.ngrok-free.app/webhook/drive
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://YOUR_NGROK_URL/webhook/drive")

# ── Paths ───────────────────────────────────────────────────────────────────
DOWNLOADS_DIR = BASE_DIR / "downloads"
CHROMA_DIR = BASE_DIR / "chroma_db"
PAGE_TOKEN_FILE = BASE_DIR / "page_token.json"
CHANNEL_STATE_FILE = BASE_DIR / "channel_state.json"

# ── Embedding model ─────────────────────────────────────────────────────────
# Free local model — no API key needed.
# Alternatives: "text-embedding-3-small" with OpenAIEmbeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")