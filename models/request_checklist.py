from pydantic import BaseModel

class Request(BaseModel):
    request_id: int
    checklist: str