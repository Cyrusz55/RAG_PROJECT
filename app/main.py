from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.ingestion import extract_text, chunk_text
from app.vectorestore import add_chunks,search_chunks
from app.rag import generate_answer

app = FastAPI(title="Document Intelligence API")

# Add CORS middleware
cors_origin_regex = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 4

@app.get("/")
async def root():
    """Serve the frontend index.html"""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "interdoc", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"status": "alive"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text(file.filename, contents)
    # chunks - list of text chunks embed and store
    chunks = chunk_text(text)
    # n - integer count of chunks that were succefully added
    n = add_chunks(doc_id=file.filename, chunks=chunks)
    # return JSON response back to whoever calls /upload endpoint
    return {"filename": file.filename, "chunks_created": n}

@app.post("/query")
async def query_documents(request: QueryRequest):
    results = search_chunks(request.question, top_k=request.top_k)
    return generate_answer(request.question, results)
