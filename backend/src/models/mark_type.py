from typing import Optional
from pydantic import BaseModel

class MarkType(BaseModel):
    id: int
    name: str
    family: Optional[str]
