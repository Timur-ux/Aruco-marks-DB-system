from pydantic import BaseModel
from typing import List

from src.models.privilege import Privilege

class Access(BaseModel):
    id: int
    name: str
    privileges: List[Privilege]

