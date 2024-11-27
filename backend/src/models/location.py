from pydantic import BaseModel
import numpy as np

class Location(BaseModel):
    id: int
    name: str
    min_pos: np.ndarray
    max_pos: np.ndarray
