from pydantic import BaseModel
from typing import List, Optional

class Request_Checklist_As_List(BaseModel):
    request_id: Optional[int] = None
    topic_id: Optional[int] = None
    checklist: List[str]