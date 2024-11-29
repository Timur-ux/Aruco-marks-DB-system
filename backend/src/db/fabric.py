from src.models.privilege import Privilege
from src.core.errors import AccessError, DataBaseError, NotFoundError
from src.models.access import Access
from src.models.user import User
import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor

from typing import List

def printError(table: str, error: Exception):
    print(f"Error while requesting to {table}, error text: {error.args}")

def privilegeFabric(cursor: DictCursor, ids: List[int]) -> List[Privilege]:
    print("Required privileges: ", ids)
    try:
        sql = "select * from privilege where id in %s;"
        cursor.execute(sql, (tuple(ids), ))
    except Exception as e:
        printError("privilege", e)
        raise DataBaseError("database error")

    privileges: List[Privilege] = []
    for id, name in cursor.fetchall():
        privileges.append(Privilege(id=id, name=name))

    return privileges



def accessFabric(cursor: DictCursor, access_: str):
    try:
        cursor.execute("select * from access where name = %s;", (access_,))
        access = cursor.fetchone()

        if(access is None):
            raise NotFoundError("Invalid access")

        privileges = privilegeFabric(cursor, access["privileges"])
    except Exception as e:
        printError("access", e)
        raise DataBaseError("database error")

    return Access(id = access["id"], name = access["name"], privileges=privileges)

def userFabric(cursor: DictCursor, access_: str, login: str, password: str):
    access = accessFabric(cursor, access_)
    # TODO: Some logic to validate access and login and password
    try:
        cursor.execute("select * from users where login = %s and password = %s;", (login, password))
    except Exception as e:
        printError("users", e)
        raise DataBaseError("database error")
    
    users = cursor.fetchall();
    if(users == []):
        raise NotFoundError("Invalid user login and/or password")

    for user in users:
        if(user['access_level'] == access.id):
            return User(id=user["id"], login=user["login"], password=password, access=access)

    raise AccessError("Access denied")
