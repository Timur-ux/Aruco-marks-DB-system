from pydantic import BaseModel, field_serializer
from typing import Dict
from datetime import datetime

class TokenData(BaseModel):
    user_id: int

class TokenPayload(BaseModel):
    data:Dict
    expired:datetime

    @field_serializer("expired")
    def serialize_expired(self, expired:datetime, _info):
        return expired.timestamp()
