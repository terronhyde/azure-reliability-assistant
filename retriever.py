from typing import Tuple, List
from indexer import chunks, VECTOR_STORE_PATH, EMBEDDING_DIM, get_embeddings
import faiss
import numpy as np
from openai import OpenAI

def retrieve_answer(query: str) -> Tuple[str, List[str]]:
    # Load FAISS index and chunk metadata
    if not chunks:
        return "No documents indexed yet.", []
    try:
        index = faiss.read_index(VECTOR_STORE_PATH)
    except Exception:
        return "Vector store not found. Please run /index first.", []
    # Embed query
    q_emb = get_embeddings([query])
    D, I = index.search(q_emb, 3)  # top-3
    top_chunks = [chunks[i] for i in I[0] if i < len(chunks)]
    # Build prompt
    context = "\n---\n".join([c["text"] for c in top_chunks])
    prompt = f"Answer the question using only the context below.\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    # Call OpenAI for answer
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.2
    )
    answer = completion.choices[0].message.content.strip() # type: ignore
    sources = list({c["file"] for c in top_chunks})
    return answer, sources
