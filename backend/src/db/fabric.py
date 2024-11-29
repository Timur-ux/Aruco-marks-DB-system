from src.core.errors import AccessError, DataBaseError, NotFoundError

from src.models.privilege import Privilege
from src.models.access import Access
from src.models.mark import Mark
from src.models.user import User
from src.models.mark_type import MarkType
from src.models.location import Location

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
        raise DataBaseError()

    privileges: List[Privilege] = []
    for id, name in cursor.fetchall():
        print(id, name)
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
        raise DataBaseError()

    result = Access(id = access["id"], name = access["name"], privileges=privileges)
    print("Access: ", result)
    return result

def userFabric(cursor: DictCursor, access_: str, login: str, password: str):
    access = accessFabric(cursor, access_)
    # TODO: Some logic to validate access and login and password
    try:
        cursor.execute("select * from users where login = %s and password = %s;", (login, password))
    except Exception as e:
        printError("users", e)
        raise DataBaseError()
    
    users = cursor.fetchall();
    if(users == []):
        raise NotFoundError("Invalid user login and/or password")

    for user in users:
        if(user['access_level'] == access.id):
            return User(id=user["id"], login=user["login"], password=password, access=access)

    raise AccessError("Access denied")

def locationFabric(cursor: DictCursor, id: int):
    try:
        cursor.execute("select * from locations where id = %s", (id, ))
    except Exception as e:
        printError("locations", e)
        raise DataBaseError()
    
    row = cursor.fetchone()
    if(row is None):
        raise NotFoundError("No such location")

    return Location(id = id, name = row["name"], min_pos=row["min_pos"], max_pos=row["max_pos"])

def mark_typeFabric(cursor: DictCursor, id: int):
    try:
        cursor.execute("select * from mark_types where id = %s", (id, ))
    except Exception as e:
        printError("mark_types", e)
        raise DataBaseError()
    
    row = cursor.fetchone()
    if(row is None):
        raise NotFoundError("No such mark_type")

    return MarkType(id = id, name=row["name"], family=row["family"])

def markFabric(cursor: DictCursor, id: int):
    try:
        cursor.execute("select * from marks where id = %s", (id, ))
        row = cursor.fetchone()
        if(row is None):
            raise NotFoundError("No such mark_type")
        location = locationFabric(cursor, row["location_id"])
        mark_type = mark_typeFabric(cursor, row["mark_type"])
    except Exception as e:
        printError("marks", e)
        raise DataBaseError()
    

    return Mark(id = id, mark_id=row["mark_id"], mark_type=mark_type, location=location, last_pos=row["last_position"])
