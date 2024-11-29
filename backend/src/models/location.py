from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    id: int
    name: str
    min_pos: List[float]
    max_pos: List[float]
