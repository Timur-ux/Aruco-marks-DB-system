from pydantic import BaseModel
from typing import List

from src.models.mark import Mark


class ListOfMarks(BaseModel):
    marks: List[Mark]
