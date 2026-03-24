from pydantic import BaseModel

class Request(BaseModel):
    topic_id: int
    request_id: int
    collection_id: str
    title: str
    background: str
    problem_statement: str
    limit: int