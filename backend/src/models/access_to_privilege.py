from pydantic import BaseModel

class Access_to_privilege(BaseModel):
    access_id: int
    privilege_id: int
