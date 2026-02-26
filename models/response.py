from pydantic import BaseModel
from typing import List, Dict, Optional

class Metadata(BaseModel):
    team_id: str
    run_id: str
    topic_id: str
    task:  Optional[str] = None
    request_id: str
    narrative_id: str

class ResponseItem(BaseModel):
    citations: list | dict
    text: str

class Document(BaseModel):
    id: str
    text: str
    url: Optional[str] = None

class Response(BaseModel):
    is_ragtime: bool
    metadata: Metadata
    responses: List[ResponseItem]
    answer: List[ResponseItem]
    references: List[str] = [] 
    documents: Dict[str, Document] = {}