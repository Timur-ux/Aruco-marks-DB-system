from pydantic import BaseModel
import numpy as np

from src.models.location import Location
from src.models.mark_type import MarkType

class Mark(BaseModel):
    id: int
    mark_id: int
    mark_type: MarkType
    location: Location
    last_pos: np.ndarray

