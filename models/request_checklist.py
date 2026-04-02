from pydantic import BaseModel
from typing import Optional

class Request_Checklist(BaseModel):
    request_id: Optional[int] = None
    topic_id: Optional[int] = None
    checklist: str