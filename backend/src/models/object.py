from typing import List, Optional
from pydantic import BaseModel

class Object(BaseModel):
    id: int
    name: Optional[str]
    size: Optional[List[float]]
    location: int
    last_pos: List[float]
