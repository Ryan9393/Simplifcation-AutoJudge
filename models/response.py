from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class Metadata(BaseModel):
    team_id: Optional[str] = None
    run_id: Optional[str] = None
    topic_id: Optional[str] = None
    task: Optional[str] = None
    request_id: Optional[str] = None
    narrative_id: Optional[str] = None

class ResponseItem(BaseModel):
    text: str
    citations: Union[Dict[str, float], list] = {}

class Document(BaseModel):
    id: str
    text: str
    url: Optional[str] = None

class Response(BaseModel):
    topic_id: Optional[str] = None
    responses: List[ResponseItem]
    metadata: Optional[Metadata] = None
    answer: Optional[List[ResponseItem]] = None
    references: Optional[List[str]] = None
    documents: Optional[Dict[str, Document]] = None
    is_ragtime: Optional[bool] = None