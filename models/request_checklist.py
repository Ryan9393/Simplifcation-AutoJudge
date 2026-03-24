from pydantic import BaseModel

class Request_Checklist(BaseModel):
    request_id: int
    checklist: str