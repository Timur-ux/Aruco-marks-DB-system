from pydantic import BaseModel

from src.models.mark_type import MarkType

class Mark(BaseModel):
    id: int
    mark_id: int
    mark_type: int
