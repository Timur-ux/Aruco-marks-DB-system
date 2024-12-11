from typing import List
from pydantic import BaseModel

class DumpsListResponse(BaseModel):
    dumps: List[str]

