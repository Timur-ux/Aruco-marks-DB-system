from pydantic import BaseModel, SerializeAsAny
from typing import List
from src.models.request import Request

class Message(BaseModel):
    type: str
    data: SerializeAsAny[BaseModel]

class ErrorMessage(BaseModel):
    text: str
    code: int

class DataMessage(BaseModel):
    data: str

class AuthMessage(DataMessage):
    token: str

class RequestsListMessage(BaseModel):
    requests: List[Request]

class TabledMessage(BaseModel):
    columns: List[str]
    rows: List[SerializeAsAny[BaseModel]]

