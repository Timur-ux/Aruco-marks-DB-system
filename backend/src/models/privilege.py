from pydantic import BaseModel

class Privilege(BaseModel):
    id: int
    name: str


