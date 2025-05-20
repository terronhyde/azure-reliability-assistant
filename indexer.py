from typing import List, Dict
from datetime import datetime
import os
from docx import Document
from pptx import Presentation
import faiss
import numpy as np
from openai import OpenAI

# Globals for MVP
VECTOR_STORE_PATH = "vector.index"
CHUNK_SIZE = 500  # characters
EMBEDDING_DIM = 1536  # OpenAI text-embedding-ada-002
EMBED_MODEL = "text-embedding-ada-002"

# In-memory store for file metadata and chunks
indexed_files = []  # List[Dict]
chunks = []         # List[Dict] with keys: text, file, chunk_id

# Helper: extract text from docx

def extract_docx_text(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# Helper: extract text from pptx

def extract_pptx_text(path):
    prs = Presentation(path)
    texts = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                texts.append(shape.text)
    return "\n".join([t for t in texts if t.strip()])

# Helper: chunk text

def chunk_text(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Helper: get OpenAI embeddings

def get_embeddings(texts: List[str]) -> np.ndarray:
    client = OpenAI()
    response = client.embeddings.create(input=texts, model=EMBED_MODEL)
    return np.array([e.embedding for e in response.data], dtype=np.float32)

# Main: index documents

def index_documents() -> List[str]:
    global indexed_files, chunks
    indexed_files = []
    chunks = []
    all_texts = []
    chunk_meta = []
    for folder in ["data/qdd", "data/qcp", "data/plr", "data/opsex"]:
        if not os.path.exists(folder):
            continue
        for fname in os.listdir(folder):
            if fname.endswith(".pptx") or fname.endswith(".docx"):
                path = os.path.join(folder, fname)
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
                indexed_files.append({"filename": path, "last_modified": mtime})
                # Extract text
                if fname.endswith(".docx"):
                    text = extract_docx_text(path)
                else:
                    text = extract_pptx_text(path)
                # Chunk and collect
                for i, chunk in enumerate(chunk_text(text)):
                    all_texts.append(chunk)
                    chunk_meta.append({"text": chunk, "file": path, "chunk_id": i})
    # Embed and build FAISS index
    if all_texts:
        embs = get_embeddings(all_texts)
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        index.add(embs)
        faiss.write_index(index, VECTOR_STORE_PATH)
        chunks = chunk_meta
    return [f["filename"] for f in indexed_files]

# Main: get indexed files

def get_indexed_files() -> List[Dict]:
    return indexed_files
