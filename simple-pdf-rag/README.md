# PDF RAG Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot built using:

- LangChain
- ChromaDB
- OpenAI GPT-4o-mini
- HuggingFace Embeddings

The chatbot loads a PDF, converts it into embeddings, stores them in a vector database, retrieves relevant chunks based on user questions, and generates answers using GPT-4o-mini.

---

# Features

- PDF document ingestion
- Text chunking
- Embedding generation
- Local vector database using ChromaDB
- Semantic similarity search
- Conversational question answering
- OpenAI GPT-4o-mini integration

---

# Project Structure

```bash
.
├── ingest-pdf.py
├── chatbot.py
├── pdfRead.pdf
├── chroma_db/
├── .env
├── .gitignore
└── README.md
```

---

# Tech Stack

| Component | Technology |
|---|---|
| LLM | GPT-4o-mini |
| Framework | LangChain |
| Vector DB | ChromaDB |
| Embeddings | HuggingFace Embeddings |
| PDF Loader | PyPDFLoader |

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repo-url>

cd <repo-name>
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install langchain-huggingface
pip install langchain-chroma
pip install langchain-text-splitters
pip install chromadb
pip install sentence-transformers
pip install pypdf
pip install python-dotenv
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

# Add PDF

Place your PDF inside the project directory and update:

```python
pdf_path = "./pdfRead.pdf"
```

inside `ingest-pdf.py`.

---

# Store PDF Embeddings

Run:

```bash
python ingest-pdf.py
```

This will:
- load PDF
- split into chunks
- generate embeddings
- store vectors in ChromaDB

---

# Start Chatbot

Run:

```bash
python chatbot.py
```

---

# Example

```text
You: What is the leave policy?

Bot: Employees can apply for leave through the HR portal...
```

---

# How It Works

```text
PDF
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Retriever
 ↓
GPT-4o-mini
 ↓
Final Answer
```

---

# Important Notes

- ChromaDB runs locally, no API key required.
- HuggingFace embeddings are free and run locally.
- Only GPT-4o-mini API usage consumes OpenAI credits.

---

# Configuration

Inside `chatbot.py`:

```python
TOP_K_DOCS = 4
```

Controls how many relevant chunks are retrieved.

