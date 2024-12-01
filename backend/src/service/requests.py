from contextlib import closing
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor
from psycopg2.sql import SQL, Placeholder, Identifier, Composed
import json

from pydantic import SerializeAsAny, TypeAdapter, BaseModel

from src.models.request import AddNewMarkRequest, DeleteMarkRequest, Request, AuthRequest
from src.models.message import AuthMessage, DataMessage, Message, RequestsListMessage, Status, StatusMessage, TabledMessage
from src.models.user import User
from src.core.errors import AlreadyExistError, DataBaseError, NotFoundError
from src.db.fabric import PrivilegeFabric, UserActionsFabric, accessFabric, markFabric, UserFabric, printError
from typing import List, Dict

from datetime import datetime

import src.db.sessionManager as sm

from devtools import pprint

class RequestProccessor:
    def __init__(self, sessionManager: sm.SessionManager):
        self.sessionManager = sessionManager

    def onAction(self, cursor: DictCursor, action: str, user_id: int = -1, time: datetime = datetime.now()) -> None:
        try:
            cursor.execute("insert into user_actions(action, user_id, time) values (%s, %s, %s)", (action, user_id, time))
        except Exception as e:
            printError("user_actions", e)
            raise DataBaseError()

    def auth(self, access: str, login: str, password: str) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                user = UserFabric.byData(cursor, access, login, password)

                self.onAction(cursor, "auth", user.id)
                return Message(type="Authentication", data = AuthMessage(
                    data = f"{user.login} is logged in successfully",
                    token = "some access token"
                    ))

    def register(self, access: str, login: str, password: str) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                try:
                    user = UserFabric.byData(cursor, access, login, password)
                except NotFoundError:
                    accessObj = accessFabric(cursor, access)
                    try:
                        cursor.execute(
                            "insert into users(access_level, login, password) values (%s, %s, %s);"
                            , (accessObj.id, login, password))
                    except Exception as e:
                        printError("users", e)
                        raise DataBaseError()

                    user = UserFabric.byData(cursor, access, login, password)
                    self.onAction(cursor, "register", user.id)

                    return StatusMessage(status=Status.Success, message= f"{login} is registred successfully")

                # if user exist raise error
                raise AlreadyExistError(f"{user.login} is already exist")

    def getRequestsList(self, access_: str) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True

                print("Required request list for access: ", access_)
                access = accessFabric(cursor, access_)
                privileges = PrivilegeFabric.fromAccess(cursor, access)

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

                self.onAction(cursor, "get requests list")
        return Message(type="RequestsList", data=RequestsListMessage(requests=requests))

    def getMarksList(self) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                try:
                    cursor.execute("select id from marks;")
                    ids = cursor.fetchall()

                    cursor.execute("select column_name from information_schema.columns where table_name=%s", ("marks", ))
                    columns: List[str] = list(map(lambda x: x[0], cursor.fetchall()))
                except Exception as e:
                    printError("marks, information_schema", e)
                    raise DataBaseError()

                marks = []
                for item in ids:
                    try:
                        marks.append(markFabric(cursor, item["id"]))
                    except Exception as e:
                        print("Warn: can't create mark object with id: ", item["id"], "\nError message: ", e.args)
                        continue

                result = TabledMessage(columns=columns, rows=marks).asMessage()
                self.onAction(cursor, "get marks list")

                return result

    def getMarkData(self, mark_id: int) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                try:
                    cursor.execute("select id from marks where mark_id=%s;", (mark_id,))
                    ids = cursor.fetchall()

                    cursor.execute("select column_name from information_schema.columns where table_name=%s", ("marks", ))
                    columns: List[str] = list(map(lambda x: x[0], cursor.fetchall()))
                except Exception as e:
                    printError("marks, information_schema", e)
                    raise DataBaseError()

                marks = []
                for item in ids:
                    try:
                        marks.append(markFabric(cursor, item["id"]))
                    except Exception as e:
                        print("Warn: can't create mark object with id: ", item["id"], "\nError message: ", e.args)
                        continue

                result = TabledMessage(columns=columns, rows=marks).asMessage()
                self.onAction(cursor, f"get mark's data with id:{mark_id}")

                return result

    def changeMarkData(self, mark_id:int, newData: Dict) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                try:
                    sql = SQL("update marks set {data} where mark_id={id};").format(
                        data=SQL(", ").join(Composed([Identifier(k), SQL(" = "), Placeholder(k)]) for k in newData.keys()),
                        id=Placeholder('mark_old_id')
                            )
                    newData['mark_old_id'] = mark_id
                    print("SQL: ", cursor.mogrify(sql, newData))
                    cursor.execute(sql, newData)
                except Exception as e:
                    printError("marks", e)
                    self.onAction(cursor, "change mark data(failed)")
                    return StatusMessage(status=Status.Failed, message="Bad mark_id or params")

                del newData["mark_old_id"]
                info = "Changed parameters:  " + "  ".join(f"{key} to {value}" for key, value in newData.items())
                self.onAction(cursor, "change mark data")
                session.commit()
                return StatusMessage(status=Status.Success, message=info)

    def addNewMark(self, markData: AddNewMarkRequest) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                try:
                    sql1 = "select * from marks where mark_id = %s;"
                    cursor.execute(sql1, (markData.mark_id, ))
                    if(cursor.fetchall() != []):
                        return StatusMessage(Status.Failed, message="Already exist")

                    dump = markData.model_dump()
                    sql2 = SQL("insert into marks(%s) values %s;")
                    print("Sql2: ", cursor.mogrify(sql2, (AsIs(", ".join(dump.keys())), tuple(dump.values()),)))
                    cursor.execute(sql2, (AsIs(", ".join(dump.keys())), tuple(dump.values()),))
                except Exception as e:
                    printError("marks", e)
                    raise DataBaseError()

                info = "Parameters:  " + "  ".join(f"{key} to {value}" for key, value in dump.items())
                self.onAction(cursor, f"add mark with id: {markData.mark_id}")
                session.commit()
                return StatusMessage(status=Status.Success, message=info)

    def deleteMark(self, markData: DeleteMarkRequest) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                try:
                    sql1 = "select * from marks where mark_id = %s;"
                    cursor.execute(sql1, (markData.mark_id, ))
                    if(cursor.fetchall() == []):
                        return StatusMessage(Status.Failed, message="Not found")

                    sql2 = SQL("delete from marks where mark_id=%s;")
                    print("Sql2: ", cursor.mogrify(sql2, (markData.mark_id, )))
                    cursor.execute(sql2, (markData.mark_id, ))
                except Exception as e:
                    printError("marks", e)
                    raise DataBaseError()

                info = "Marks with:  " + "  ".join(f"{key} to {value}" for key, value in markData.model_dump().items()) + " successfully deleted"
                self.onAction(cursor, f"delete mark with id: {markData.mark_id}")
                session.commit()
                return StatusMessage(status=Status.Success, message=info)

    def getUsersInfo(self) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True

                users: List = UserFabric.allUsers(cursor)
                if(users == []):
                    return StatusMessage(status=Status.Failed, message="No one user is found")

                columns = list(users[0].model_dump().keys())
                self.onAction(cursor, f"get all users info")
                return TabledMessage(columns=columns, rows=users).asMessage()

    def getUserInfo(self, user_id: int) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                try:
                    user = UserFabric.byId(cursor, user_id)
                except NotFoundError:
                    return StatusMessage(status=Status.Failed, message="No one user is found")

                columns = list(user.model_dump().keys())
                self.onAction(cursor, f"get user info")
                return TabledMessage(columns=columns, rows=[user]).asMessage()

    def deleteUser(self, user_id: int) -> Message:
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                try:
                    UserFabric.byId(cursor, user_id)
                except NotFoundError:
                    return StatusMessage(status=Status.Failed, message="No one user is found")

                try:
                    cursor.execute("delete from users where id=%s", (user_id, ))
                except Exception as e:
                    printError("marks", e)
                self.onAction(cursor, f"delete user with id: {user_id}")
                session.commit()
                return StatusMessage(status=Status.Success, message=f"User with id: {user_id} deleted")

    def getUsersActions(self):
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                try:
                    actions: List = UserActionsFabric.allActions(cursor)
                except NotFoundError as e:
                    return StatusMessage(status=Status.Failed, message=e.args[0])

                columns = list(actions[0].model_dump().keys())
                self.onAction(cursor, f"get all users actions")
                return TabledMessage(columns=columns, rows=actions).asMessage()


    def getUserActions(self, user_id: int):
        with closing(self.sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True
                try:
                    actions: List = UserActionsFabric.byId(cursor, user_id)
                except NotFoundError as e:
                    return StatusMessage(status=Status.Failed, message="No such user_id found")

                columns = list(actions[0].model_dump().keys())
                self.onAction(cursor, f"get user with id: {user_id} actions")
                return TabledMessage(columns=columns, rows=actions).asMessage()

    def addUser(self, access, login, password):
        with closing(self.sessionManager.createSession()) as session:
            session.autocommit = True
            try:
                self.onAction(session.cursor(cursor_factory=DictCursor), f"Add user with access{access}, login: {login}")
            except Exception as e:
                print("Add user error: ", e.args)
                raise e

        return self.register(access, login, password)
