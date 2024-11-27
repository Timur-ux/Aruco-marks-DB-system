from pydantic import BaseModel
from src.models.privilege import Privilege
from src.models.access import Access

class User(BaseModel):
    id: int
    login: str
    password: str
    access: Access

def hasAccessTo(user: User, privilege: Privilege):
    try:
        user.access.privileges.index(privilege)
    except ValueError:
        return False

    return True
