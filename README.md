# Azure Reliability Assistant

This project is structured as a monorepo with a FastAPI backend and a React TypeScript frontend.

## Structure

```
azure-reliability-assistant/
├── backend/
│   ├── main.py
│   ├── indexer.py
│   ├── retriever.py
│   ├── models.py
│   ├── mock_auth.py
│   ├── requirements.txt
│   └── data/
│       ├── qdd/
│       ├── qcp/
│       ├── plr/
│       └── opsex/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
├── .gitignore
├── README.md
└── LICENSE
```

## Backend
- Python FastAPI app for document indexing, retrieval, and OpenAI-powered Q&A.
- All backend code and data live in the `backend/` folder.

## Frontend
- React app scaffolded with TypeScript template in the `frontend/` folder.

## Setup

### Backend
```sh
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend
```sh
cd frontend
npm install
npm start
```

---

For more details, see the backend and frontend README files (if present).
