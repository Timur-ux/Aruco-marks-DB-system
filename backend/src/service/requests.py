from contextlib import aclosing
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor
from psycopg2.sql import SQL, Placeholder, Identifier, Composed
from fastapi import HTTPException, status, Response
import json

from src.models.user import User
from src.models.token import TokenData
from src.models.request import AddNewMarkRequest, DeleteMarkRequest, DumpDBRequest, Request, RestoreDumpRequest
from src.models.message import AuthMessage, Message, RequestsListMessage, Status, StatusMessage, TabledMessage, DumpsListMessage
from src.core.errors import AlreadyExistError, DataBaseError
from src.db.fabric import PrivilegeFabric, UserActionsFabric, AccessFabric, markFabric, UserFabric, printError
from typing import List, Dict

from src.service.password import get_password_hash
from src.service.jwt import create_access_token

from datetime import datetime

import src.db.sessionManager as sm
from src.service.backups import default_backuper

from devtools import pprint
from fastapi import status

import asyncio
import aiopg


class RequestProccessor:
    def __init__(self, sessionManager: sm.SessionManager):
        self.sessionManager = sessionManager

    async def validate_access(self, cursor: DictCursor, user: User, minimal_access: str) -> bool:
        user_access = await AccessFabric.byId(cursor, user.access_level)
        required_access = await AccessFabric.byName(cursor, minimal_access)
        print("User_access: ", user_access.id,
              "Required: ", required_access.id)

        return user_access.id >= required_access.id

    async def onAction(self, cursor: DictCursor, action: str, user_id: int = -1, time: datetime = datetime.now()) -> None:
        try:
            await cursor.execute(
                "insert into user_actions(action, user_id, time) values (%s, %s, %s)", (action, user_id, time))
        except Exception as e:
            printError("user_actions", e)
            raise DataBaseError()

    async def auth(self,  access_: str, login: str, password: str, response: Response) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                user = await UserFabric.auth(cursor, login, password)
                access = await AccessFabric.byName(cursor, access_)
                if user is None:
                    raise HTTPException(
                        status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")
                if access.id != user.access_level:
                    raise HTTPException(
                        status.HTTP_401_UNAUTHORIZED, detail="Incorrect access")

                try:
                    token = create_access_token(
                        TokenData(user_id=user.id).model_dump())
                except Exception as e:
                    print("Exception while creating token: ", e.args)
                    raise HTTPException(
                        status.HTTP_401_UNAUTHORIZED, detail="Token creating failed")

                print("Generated token: ", token)
                response.set_cookie(key="access_token",
                                    value=token, httponly=True)
                await self.onAction(cursor, "auth", user.id)
                return Message(type="Authentication", data=AuthMessage(
                    data=f"{user.login} is logged in successfully",
                ))

    async def register(self, access: str, login: str, password: str, user: User | None) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                if (access != "user"):
                    if user is None or not await self.validate_access(cursor, user, "administrator"):
                        raise HTTPException(
                            status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    user = await UserFabric.byData(cursor, access, login, password)
                except Exception:
                    accessObj = await AccessFabric.byName(cursor, access)
                    try:
                        await cursor.execute(
                            "insert into users(access_level, login, password) values (%s, %s, %s);", (accessObj.id, login, get_password_hash(password)))
                    except Exception as e:
                        printError("users", e)
                        raise DataBaseError()

                    user = await UserFabric.auth(cursor, login, password)
                    if (user is None):
                        raise DataBaseError("failed to add user to db")
                    await self.onAction(cursor, "register", user.id)

                    return StatusMessage(status=Status.Success, message=f"{login} is registred successfully")

                # if user exist raise error
                raise AlreadyExistError(f"{user.login} is already exist")

    async def getRequestsList(self, access_: str, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                if not await self.validate_access(cursor, user, access_):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")

                print("Required request list for access: ", access_)
                access = await AccessFabric.byName(cursor, access_)
                privileges = await PrivilegeFabric.fromAccess(cursor, access)

                requests: List[Request] = []
                with open("./requests.json") as file:
                    allRequests = json.load(file)
                    for privilege in privileges:
                        for requestData in allRequests[privilege.name]:
                            print("Request: ", end="")
                            pprint(Request(**requestData))
                            requests.append(Request(**requestData))

                print("Requests: ", end="")
                pprint(requests)

                await self.onAction(cursor, "get requests list", user.id)
        return Message(type="RequestsList", data=RequestsListMessage(requests=requests))

    async def getMarksList(self, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "user"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await cursor.execute("select id from marks;")
                    ids = await cursor.fetchall()

                    await cursor.execute(
                        "select column_name from information_schema.columns where table_name=%s", ("marks", ))
                    columns: List[str] = list(
                        map(lambda x: x[0], await cursor.fetchall()))
                except Exception as e:
                    printError("marks, information_schema", e)
                    raise DataBaseError()

                marks = []
                for item in ids:
                    try:
                        marks.append(await markFabric(cursor, item["id"]))
                    except Exception as e:
                        print("Warn: can't create mark object with id: ",
                              item["id"], "\nError message: ", e.args)
                        continue

                result = TabledMessage(columns=columns, rows=marks).asMessage()
                await self.onAction(cursor, "get marks list", user.id)

                return result

    async def getMarkData(self, mark_id: int, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "user"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await cursor.execute(
                        "select id from marks where mark_id=%s;", (mark_id,))
                    ids = await cursor.fetchall()

                    await cursor.execute(
                        "select column_name from information_schema.columns where table_name=%s", ("marks", ))
                    columns: List[str] = list(
                        map(lambda x: x[0], await cursor.fetchall()))
                except Exception as e:
                    printError("marks, information_schema", e)
                    raise DataBaseError()

                marks = []
                for item in ids:
                    try:
                        marks.append(await markFabric(cursor, item["id"]))
                    except Exception as e:
                        print("Warn: can't create mark object with id: ",
                              item["id"], "\nError message: ", e.args)
                        continue

                result = TabledMessage(columns=columns, rows=marks).asMessage()
                await self.onAction(
                    cursor, f"get mark's data with id:{mark_id}", user.id)

                return result

    async def changeMarkData(self, mark_id: int, newData: Dict, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                if not await self.validate_access(cursor, user, "redactor"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    sql = SQL("update marks set {data} where mark_id={id};").format(
                        data=SQL(", ").join(
                            Composed([Identifier(k), SQL(" = "), Placeholder(k)]) for k in newData.keys()),
                        id=Placeholder('mark_old_id')
                    )
                    newData['mark_old_id'] = mark_id
                    print("SQL: ", cursor.mogrify(sql, newData))
                    await cursor.execute(sql, newData)
                except Exception as e:
                    printError("marks", e)
                    await self.onAction(cursor, "change mark data(failed)")
                    return StatusMessage(status=Status.Failed, message="Bad mark_id or params")

                del newData["mark_old_id"]
                info = "Changed parameters:  " + \
                    "  ".join(f"{key} to {value}" for key,
                              value in newData.items())
                await self.onAction(cursor, "change mark data", user.id)
                return StatusMessage(status=Status.Success, message=info)

    async def addNewMark(self, markData: AddNewMarkRequest, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                if not await self.validate_access(cursor, user, "redactor"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    sql1 = "select * from marks where mark_id = %s;"
                    await cursor.execute(sql1, (markData.mark_id, ))
                    if (await cursor.fetchall() != []):
                        return StatusMessage(Status.Failed, message="Already exist")

                    dump = markData.model_dump()
                    sql2 = SQL("insert into marks(%s) values %s;")
                    print("Sql2: ", cursor.mogrify(
                        sql2, (AsIs(", ".join(dump.keys())), tuple(dump.values()),)))
                    await cursor.execute(
                        sql2, (AsIs(", ".join(dump.keys())), tuple(dump.values()),))
                except Exception as e:
                    printError("marks", e)
                    raise DataBaseError()

                info = "Parameters:  " + \
                    "  ".join(f"{key} to {value}" for key,
                              value in dump.items())
                await self.onAction(
                    cursor, f"add mark with id: {markData.mark_id}", user.id)
                return StatusMessage(status=Status.Success, message=info)

    async def deleteMark(self, markData: DeleteMarkRequest, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                if not self.validate_access(cursor, user, "redactor"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    sql1 = "select * from marks where mark_id = %s;"
                    await cursor.execute(sql1, (markData.mark_id, ))
                    if (await cursor.fetchall() == []):
                        return StatusMessage(Status.Failed, message="Not found")

                    sql2 = SQL("delete from marks where mark_id=%s;")
                    print("Sql2: ", cursor.mogrify(sql2, (markData.mark_id, )))
                    await cursor.execute(sql2, (markData.mark_id, ))
                except Exception as e:
                    printError("marks", e)
                    raise DataBaseError()

                info = "Marks with:  " + \
                    "  ".join(f"{key} to {value}" for key, value in markData.model_dump(
                    ).items()) + " successfully deleted"
                await self.onAction(
                    cursor, f"delete mark with id: {markData.mark_id}", user.id)
                return StatusMessage(status=Status.Success, message=info)

    async def getUsersInfo(self, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")

                users: List = await UserFabric.allUsers(cursor)
                if (users == []):
                    return StatusMessage(status=Status.Failed, message="No one user is found")

                columns = list(users[0].model_dump().keys())
                await self.onAction(cursor, f"get all users info", user.id)
                return TabledMessage(columns=columns, rows=users).asMessage()

    async def getUserInfo(self, user_id: int, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    user = await UserFabric.byId(cursor, user_id)
                except Exception:
                    return StatusMessage(status=Status.Failed, message="No one user is found")

                columns = list(user.model_dump().keys())
                await self.onAction(cursor, f"get user info", user.id)
                return TabledMessage(columns=columns, rows=[user]).asMessage()

    async def deleteUser(self, user_id: int, user: User) -> Message:
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:
                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await UserFabric.byId(cursor, user_id)
                except Exception:
                    return StatusMessage(status=Status.Failed, message="No one user is found")

                try:
                    await cursor.execute(
                        "delete from users where id=%s", (user_id, ))
                except Exception as e:
                    printError("marks", e)
                await self.onAction(
                    cursor, f"delete user with id: {user_id}", user.id)
                return StatusMessage(status=Status.Success, message=f"User with id: {user_id} deleted")

    async def getUsersActions(self, user: User):
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    actions: List = await UserActionsFabric.allActions(cursor)
                except Exception as e:
                    return StatusMessage(status=Status.Failed, message=e.args[0])

                columns = list(actions[0].model_dump().keys())
                await self.onAction(cursor, f"get all users actions", user.id)
                return TabledMessage(columns=columns, rows=actions).asMessage()

    async def getUserActions(self, user_id: int, user: User):
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    actions: List = await UserActionsFabric.byId(cursor, user_id)
                except Exception:
                    return StatusMessage(status=Status.Failed, message="No such user_id found")

                columns = list(actions[0].model_dump().keys())
                await self.onAction(
                    cursor, f"get user with id: {user_id} actions", user.id)
                return TabledMessage(columns=columns, rows=actions).asMessage()

    async def addUser(self, access, login, password, user: User):
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await self.onAction(
                        cursor, f"Add user with access {access}, login: {login}", user.id)
                except Exception as e:
                    print("Add user error: ", e.args)
                    raise e

        return await self.register(access, login, password, user)

    async def createDBDump(self, data: DumpDBRequest, user: User):
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await self.onAction(
                        cursor, f"dump database by {user.login}", user.id)
                    default_backuper.dump(data.suffix)
                    return StatusMessage(status=Status.Success, message="dump has created")
                except Exception as e:
                    print("ERROR: Dump db:", e.args)
                    return StatusMessage(status=Status.Failed, message="dump has not created")

    async def getDBDumps(self, user: User):
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await self.onAction(
                        cursor, f"get db dumps list by {user.login}", user.id)
                    dumps = default_backuper.get_dumps()
                    return DumpsListMessage(dumps=dumps).asMessage()
                except Exception as e:
                    print("ERROR: get db dumps:", e.args)
                    raise e

    async def restoreDBDums(self, data: RestoreDumpRequest, user: User):
        async with await self.sessionManager.createSession() as session:
            async with session.cursor(cursor_factory=DictCursor) as cursor:

                if not await self.validate_access(cursor, user, "administrator"):
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN, "Access denied")
                try:
                    await self.onAction(
                        cursor, f"dump database with id {data.dump_id} by {user.login}", user.id)
                    dumps = default_backuper.get_dumps()
                    if data.dump_id in range(len(dumps)):
                        default_backuper.load(dumps[data.dump_id])
                        await self.onAction(
                            cursor, f"dump database with id {data.dump_id} by {user.login}", user.id)
                        return StatusMessage(status=Status.Success, message=f"dump: {dumps[data.dump_id]} has restored")
                    else:
                        await self.onAction(
                            cursor, f"Failed[incorrect dump_id]: dump database not created", user.id)
                        return StatusMessage(status=Status.Failed, message=f"Incorrect dump_id")
                except Exception as e:
                    print("ERROR: restore db dump:", e.args)
                    raise e
