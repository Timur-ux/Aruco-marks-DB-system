from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    access_level: int
    login: str
    password: str

class UserAction(BaseModel):
    id: int
    action: str
    user_id: int
    time: datetime
