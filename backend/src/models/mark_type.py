from typing import Optional
from pydantic import BaseModel
import numpy as np

class MarkType(BaseModel):
    id: int
    name: str
    family: Optional[str]
