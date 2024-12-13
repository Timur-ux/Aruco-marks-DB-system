from pydantic import BaseModel, field_serializer
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

    @field_serializer("time")
    def serialize_time(self, time: datetime, _info):
        return time.strftime("%Y-%m-%d %H:%M:%S")
