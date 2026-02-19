from pydantic import BaseModel
from typing import List

class Request(BaseModel):
    topic_id: int
    request_id: int
    collection_id: str
    title: str
    background: str
    problem_statement: str
    limit: int