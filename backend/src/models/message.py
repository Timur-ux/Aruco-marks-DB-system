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
        super().__init__(type="Tabled", data=TabledMessage(columns=[
            "Status", "Info"], rows=[self.StatusData(status=status, info=message)]))


class DumpsListMessage(TabledMessage):
    class DumpListItem(BaseModel):
        dump_id: int
        dump_name: str

    def __init__(self, dumps: List[str]):
        columns = ["dump_id", "dump_name"]
        rows = []
        for i, name in enumerate(dumps):
            rows.append(self.DumpListItem(dump_id=i, dump_name=name))
        super().__init__(columns=columns, rows=rows)
