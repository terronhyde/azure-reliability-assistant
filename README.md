# azure-reliability-assistant

The Azure Reliability Assistant (ARA) is a Copilot-style internal web application for the Azure Change SRE team. It provides natural language insights from unstructured datasources, using local document parsing and retrieval-augmented generation (RAG).

## Features

- **POST /ask** — Accepts a user query, retrieves relevant chunks from indexed documents using FAISS, and returns a GPT-generated answer with sources.
- **POST /index** — Ingests and indexes all `.pptx` and `.docx` files from local folders (`/data/qdd/`, `/data/qcp/`, `/data/plr/`, `/data/opsex/`).
- **GET /sources** — Returns a list of currently indexed files and their last modified times.
- **GET /auth** — Returns a mock user identity (authentication is stubbed).

## How it Works

- **Document Parsing:** Uses `python-docx` and `python-pptx` to extract text from `.docx` and `.pptx` files.
- **Chunking:** Documents are split into manageable text chunks for embedding.
- **Embeddings & Vector Store:** Chunks are embedded using OpenAI's `text-embedding-ada-002` model and stored in a FAISS vector index for fast similarity search.
- **Retrieval & Generation:** On a user query, the top relevant chunks are retrieved and passed as context to OpenAI's GPT model to generate an answer.

## Directory Structure

- `/data/qdd/`      (contains `.pptx` files)
- `/data/qcp/`
- `/data/plr/`      (contains `.docx` files)
- `/data/opsex/`

## Dependencies

- fastapi
- uvicorn
- openai
- faiss-cpu
- python-docx
- python-pptx
- pydantic
- langchain (optional, for chaining)

## Running Locally

1. Install dependencies:
   ```sh
   python -m pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```sh
   python -m uvicorn main:app --reload
   ```
3. Use the `/index` endpoint to index your documents.
4. Use the `/ask` endpoint to query the assistant.
5. Explore the API at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Notes
- Requires an OpenAI API key set in your environment (e.g., `OPENAI_API_KEY`).
- This is an MVP and does not include production authentication or security.
- All document parsing and vector storage is local.

---

For more details, see the code in `main.py`, `indexer.py`, and `retriever.py`.
