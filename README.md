# Interdoc

Interdoc is a FastAPI-powered document Q&A app with a single-page frontend.

## Features
- Upload documents
- Ask questions grounded in uploaded content
- View citations by document and chunk index
- Single app served from FastAPI

## Run locally

```powershell
cd D:\Users\user\PycharmProjects\RAG_PROJECT
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

## Render deployment

This project is ready for a single web service on Render.

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

If you prefer, Render can also use `render.yaml`.

