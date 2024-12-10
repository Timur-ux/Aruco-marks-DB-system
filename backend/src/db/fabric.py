from fastapi import HTTPException, status
from src.core.errors import AccessError, DataBaseError, NotFoundError
from src.models.access_to_privilege import Access_to_privilege
from src.models.privilege import Privilege
from src.models.access import Access
from src.models.mark import Mark
from src.models.user import User, UserAction
from src.models.mark_type import MarkType
from src.models.location import Location

from src.service.password import verity_password

from psycopg2.extras import DictCursor
from typing import List

from devtools import pprint


def printError(table: str, error: Exception):
    print(f"Error while requesting to {table}, error text: {error.args}")


def processExecute(cursor: DictCursor, sql, table="undefined", *args):
    try:
        cursor.execute(sql, args)
    except Exception as e:
        printError(table, e)
        raise DataBaseError()

    return cursor


class PrivilegeFabric:
    idsSql = "select * from privilege where id in %s;"
    accessSql = "select * from access_to_privileges where access_id=%s;"
    table = "privilege"

    @staticmethod
    def fromIds(cursor: DictCursor, ids: List[int]) -> List[Privilege]:
        print("Required privileges: ", ids)
        cursor = processExecute(
            cursor, PrivilegeFabric.idsSql, PrivilegeFabric.table, tuple(ids))
        privileges: List[Privilege] = []
        for row in cursor.fetchall():
            privileges.append(Privilege(**row))

        return privileges

    @staticmethod
    def fromAccess(cursor: DictCursor, access: Access) -> List[Privilege]:
        print("Required privileges for access: ", access.name)
        cursor = processExecute(
            cursor, PrivilegeFabric.accessSql, PrivilegeFabric.table, access.id)
        binds: List[Access_to_privilege] = [
            Access_to_privilege(**x) for x in cursor.fetchall()]
        privileges = PrivilegeFabric.fromIds(
            cursor, [x.privilege_id for x in binds])

        print("Privileges: ")
        pprint(privileges)

        return privileges


class AccessFabric:
    byNameSql = "select * from access where name = %s;"
    byIdSql = "select * from access where id = %s"

    @staticmethod
    def byId(cursor:DictCursor, id:int) -> Access:
        try:
            cursor.execute(AccessFabric.byIdSql, (id,))
            accessData = cursor.fetchone()
            if accessData is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"No access with such id: {id}" )
        except Exception as e:
            printError("access", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

        return Access(**accessData)

    @staticmethod
    def byName(cursor:DictCursor, access_: str) -> Access:
        try:
            cursor.execute("select * from access where name = %s;", (access_,))
            access = cursor.fetchone()

            if (access is None):
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid access")
        except Exception as e:
            printError("access", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

        result = Access(**access)
        return result


class UserFabric:
    byDataSql = "select * from users where login = %s and password = %s;"
    byIdSql = "select * from users where id = %s;"
    totalSql = "select * from users;"
    authSql = "select * from users where login = %s"

    @staticmethod
    def auth(cursor: DictCursor, login: str, plain_password: str) -> User | None:
        try:
            cursor.execute(UserFabric.authSql, (login,))
        except Exception as e:
            printError("users", e)
            return None
        userData = cursor.fetchone()
        if userData is None:
            return None
        user = User(**userData)
        if not verity_password(plain_password, user.password):
            return None
        return user

    @staticmethod
    def byData(cursor: DictCursor, access_: str, login: str, password: str) -> User:
        access = AccessFabric.byName(cursor, access_)
        # TODO: Some logic to validate access and login and password
        try:
            cursor.execute(UserFabric.byDataSql, (login, password))
        except Exception as e:
            printError("users", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

        user = cursor.fetchone()
        if (user is None):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid user login and/or password")

        if (user['access_level'] == access.id):
            print("User: ", {**user})
            return User(**user)

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied")

    @staticmethod
    def byId(cursor: DictCursor, user_id: int) -> User:
        # TODO: Some logic to validate access and login and password
        try:
            cursor.execute(UserFabric.byIdSql, (user_id, ))
        except Exception as e:
            printError("users", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

        user = cursor.fetchone()
        if (user is None):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No users found with this id")

        return User(**user)

    @staticmethod
    def allUsers(cursor: DictCursor) -> List[User]:
        try:
            cursor.execute(UserFabric.totalSql)
        except Exception as e:
            printError("users", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

        return list(map(lambda x: User(**x), cursor.fetchall()))


def locationFabric(cursor: DictCursor, id: int):
    try:
        cursor.execute("select * from locations where id = %s", (id, ))
    except Exception as e:
        printError("locations", e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

    row = cursor.fetchone()
    if (row is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such location")

    return Location(**row)


def mark_typeFabric(cursor: DictCursor, id: int):
    try:
        cursor.execute("select * from mark_types where id = %s", (id, ))
    except Exception as e:
        printError("mark_types", e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

    row = cursor.fetchone()
    if (row is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such mark_type")

    # return MarkType(id = id, name=row["name"], family=row["family"])
    return MarkType(**row)


def markFabric(cursor: DictCursor, id: int):
    try:
        cursor.execute("select * from marks where id = %s", (id, ))
    except Exception as e:
        printError("marks", e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

    row = cursor.fetchone()
    if (row is None):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such mark_type")

    # return Mark(id = id, mark_id=row["mark_id"], mark_type=row["mark_type"])
    return Mark(**row)


class UserActionsFabric:
    allActionsSql = "select * from user_actions order by time desc;"
    byIdSql = "select * from user_actions where user_id=%s order by time desc;"

    @staticmethod
    def allActions(cursor: DictCursor) -> List[UserAction]:
        try:
            cursor.execute(UserActionsFabric.allActionsSql)
        except Exception as e:
            printError("user_actions", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 
        rows = cursor.fetchall()
        if (rows == []):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Actions not found")

        return list(map(lambda x: UserAction(**x), rows))

    @staticmethod
    def byId(cursor: DictCursor, user_id: int) -> List[UserAction]:
        try:
            cursor.execute(UserActionsFabric.byIdSql, (user_id, ))
        except Exception as e:
            printError("user_actions", e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) 

        rows = cursor.fetchall()
        if (rows == []):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Actions not found")

        return list(map(lambda x: UserAction(**x), rows))
