from enum import Enum
from pydantic import BaseModel
from typing import List, Dict

class RequestType(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"

class FieldType(str, Enum):
    int = "int"
    parameters = "parameters_dict"
    string = "string"
    string256 = "string(sha256)"

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

class ChangeMarkDataRequest(BaseModel):
    mark_id: int
    parameters: Dict

class AddNewMarkRequest(BaseModel):
    mark_id: int
    mark_type: int

class DeleteMarkRequest(BaseModel):
    mark_id: int

class DeleteUserRequest(BaseModel):
    user_id: int

class DumpDBRequest(BaseModel):
    suffix: str

class GetDBDumpsRequest(BaseModel):
    pass

class RestoreDumpRequest(BaseModel):
    dump_id: int
