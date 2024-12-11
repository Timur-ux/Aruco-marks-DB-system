from enum import Enum
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
    pass

class RequestsListMessage(BaseModel):
    requests: List[Request]


class TabledMessage(BaseModel):
    columns: List[str]
    rows: List[SerializeAsAny[BaseModel]]

    def asMessage(self):
        return Message(type="Tabled", data=self)


class Status(str, Enum):
    Success = "Success"
    Failed = "Failed"


class StatusMessage(Message):
    class StatusData(BaseModel):
        status: Status
        info: str

    def __init__(self, status: Status, message=""):
        super().__init__(type="Tabled", data=TabledMessage(columns=["Status", "Info"], rows=[self.StatusData(status=status, info=message)]))

class DumpListMessage(Message):
    def __init__(self, dumps: List[str]):
        super().__init__(type="DumpsList", data=)
