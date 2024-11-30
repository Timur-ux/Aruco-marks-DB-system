from enum import Enum
from pydantic import BaseModel
from typing import List

class RequestType(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"

class FieldType(str, Enum):
    int = "int"
    parameters = "parameters_dict"
    string = "string"

class Field(BaseModel):
    name: str
    type: FieldType

class Request(BaseModel):
    name: str
    type: RequestType
    uri: str
    fields: List[Field]


class AuthRequest(BaseModel):
    access: str
    login: str
    password: str
