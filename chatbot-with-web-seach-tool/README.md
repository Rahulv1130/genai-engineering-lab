# Jarvis AI Assistant

A full-stack AI assistant built using:

- Node.js
- Express.js
- Groq LLM API
- Tavily Search API
- TailwindCSS
- Vanilla JavaScript

Jarvis is a conversational AI assistant capable of:
- answering general questions
- maintaining conversation memory
- performing real-time web searches using tool

---

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend | Node.js + Express |
| LLM | Groq |
| Search Tool | Tavily |
| Frontend | HTML + TailwindCSS |
| HTTP Client | Axios |
| Cache/Memory | NodeCache |

---

# Project Structure

```bash
.
├── backend/
│   ├── server.js
│   └── chatbot.js
│
├── frontend/
│   ├── index.html
│   └── index.js
│
└── README.md
```

---

# Installation

### 1. Clone Repository

### 2. Install Backend Dependencies

```bash
npm install express cors dotenv groq-sdk prompt-sync node-cache @tavily/core
```

---

## 3. Create `.env`

Inside backend folder:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 4. Start Backend Server

```bash
node server.js
```

Server runs on:

```text
http://localhost:3001
```

---

## Frontend Setup

Simply open:

```text
frontend/index.html
```

in browser.

OR use VS Code Live Server extension.

---

# How It Works

```text
User Query
    ↓
Express Backend
    ↓
Groq LLM
    ↓
Tool Decision
    ↓
Tavily Web Search (if needed)
    ↓
Updated Context
    ↓
Final AI Response
```

---


# Tool Calling

The assistant has access to the following tool:

## webSearch({ query })

Searches the internet for:
- latest information
- real-time data
- current events

Powered by Tavily Search API.

---

# Example

```text
You: Latest AI news

Jarvis: OpenAI recently announced...
```

---

