from typing import List, Optional
import numpy
from pydantic import BaseModel

from src.models.mark import Mark

class Object(BaseModel):
    id: int
    name: Optional[str]
    size: numpy.ndarray
    marks: List[Mark]
