from typing import List, Optional
from pydantic import BaseModel

from src.models.mark import Mark

class Object(BaseModel):
    id: int
    name: Optional[str]
    size: List[float]
    marks: List[Mark]
