from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from indexer import index_documents, get_indexed_files
from retriever import retrieve_answer
from mock_auth import get_current_user

app = FastAPI()

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str
    sources: List[str]

class IndexResponse(BaseModel):
    status: str
    indexed_files: List[str]

class SourceInfo(BaseModel):
    filename: str
    last_modified: str

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, user: str = Depends(get_current_user)):
    answer, sources = retrieve_answer(request.query)
    return AskResponse(answer=answer, sources=sources)

@app.post("/index", response_model=IndexResponse)
def index(user: str = Depends(get_current_user)):
    files = index_documents()
    return IndexResponse(status="success", indexed_files=files)

@app.get("/sources", response_model=List[SourceInfo])
def sources(user: str = Depends(get_current_user)):
    return get_indexed_files()

@app.get("/auth")
def auth():
    return {"user": "mock_user"}
