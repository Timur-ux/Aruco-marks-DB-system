from pydantic import BaseModel

class Access(BaseModel):
    id: int
    name: str

