from pydantic import BaseModel
from typing import Optional

class KeyCreateRequest(BaseModel):
    type: str
    size: Optional[int] = None
    purpose: str
