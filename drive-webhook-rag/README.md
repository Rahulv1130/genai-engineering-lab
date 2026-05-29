# Google Drive Auto-Embedder RAG

Automatically monitor a Google Drive folder for newly uploaded or updated files, download supported documents, generate embeddings using HuggingFace models, and store them in ChromaDB for Retrieval-Augmented Generation (RAG) applications.

## Features

* 📂 Monitor a Google Drive folder in real-time using Drive Push Notifications
* 🔔 Automatic webhook handling via FastAPI
* 📥 Download newly added or modified files from Google Drive
* ✂️ Split documents into chunks using LangChain
* 🧠 Generate embeddings using HuggingFace Sentence Transformers
* 🗄️ Store embeddings in ChromaDB
* 🌐 Public webhook exposure using ngrok
* 🔄 Automatic renewal of Google Drive watch channels

---

## Supported File Types

| Type          | Extension         |
| ------------- | ----------------- |
| PDF           | .pdf              |
| Word          | .docx             |
| Text          | .txt              |
| Markdown      | .md               |
| CSV           | .csv              |
| Google Docs   | Exported as .docx |
| Google Sheets | Exported as .csv  |

---

## Project Structure

```bash
drive-webhook-rag/
│
├── main.py                 # FastAPI application
├── setup.py                # Initial setup and watch registration
├── drive_client.py         # Google Drive API integration
├── watcher.py              # Watch channel management
├── embedder.py             # Document processing & embeddings
├── config.py               # Environment configuration
│
├── downloads/              # Downloaded Drive files
├── chroma_db/              # ChromaDB persistence
│
├── page_token.json         # Drive changes token
├── channel_state.json      # Active watch channel state
│
├── credentials.json        # Google OAuth credentials
├── token.json              # OAuth access token
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```




---

## Installation

- Clone Repository

- Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
uv sync
```

---

## Google Cloud Setup

### Enable APIs

Enable:

* Google Drive API

### Create OAuth Credentials

Create:

```text
OAuth Client ID
Application Type: Desktop App
```

Download the credentials and save as:

```text
credentials.json
```

in the project root.

---

## Environment Variables

Create a `.env` file:

```env
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

WATCHED_FOLDER_ID=<YOUR_FOLDER_ID>

WEBHOOK_URL=https://poet-walnut-eastward.ngrok-free.dev/webhook/drive

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## Running ngrok with Docker

Start ngrok:

```bash
docker compose up -d
```

ngrok dashboard:

```text
http://localhost:4040
```

---

## Running the Application

### Step 1 — Start FastAPI

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 2 — Register Google Drive Watch

```bash
python setup.py
```

This will:

* Authenticate with Google Drive
* Save the current page token
* Register a webhook watch channel

Example:

```text
Channel ID : xxxxx
Resource ID: xxxxx
Expires    : xxxxx
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "running"
}
```

### Drive Webhook

```http
POST /webhook/drive
```

Receives Google Drive push notifications.

---