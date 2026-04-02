from pydantic import BaseModel
from typing import Optional

class Request(BaseModel):
    topic_id: str
    title: str
    background: str
    problem_statement: str
    limit: int
    request_id: Optional[int] = None
    collection_id: Optional[str] = None