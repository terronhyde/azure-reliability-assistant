from pydantic import BaseModel
from typing import List

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
