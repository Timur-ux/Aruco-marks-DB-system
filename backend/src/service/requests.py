from contextlib import closing
from psycopg2.extras import DictCursor
import json

from src.models.request import Request
from src.models.message import AuthMessage, DataMessage, ErrorMessage, Message, RequestsListMessage, TabledMessage
from src.core.errors import AccessError, AlreadyExistError, BackendError, DataBaseError, NotFoundError
from src.db.fabric import accessFabric, markFabric, userFabric
from src.models.listOfMarks import ListOfMarks
from typing import List

import src.db.sessionManager as sm

from devtools import pprint

def processAuth(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True
            user = userFabric(cursor, access, login, password)

            return Message(type="Authentication", data = AuthMessage(
                data = f"{user.login} is logged in successfully",
                token = "some access token"
                ))

def processRegister(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True
            try:
                user = userFabric(cursor, access, login, password)
            except NotFoundError as e:
                accessObj = accessFabric(cursor, access)
                try:
                    cursor.execute(
                        "insert into users(access_level, login, password) values (%s %s %s);"
                        , (accessObj.id, login, password))
                except Exception as e:
                    raise DataBaseError()

                return Message(type="Registration", data=DataMessage(data = f"{login} is registred successfully"))

            # if user exist raise error
            raise AlreadyExistError(f"{user.login} is already exist")

def processGetRequestsList(sessionManager: sm.SessionManager, access_: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True

            print("Required request list for access: ", access_)
            access = accessFabric(cursor, access_)

            requests: List[Request] = []
            with open("./requests.json") as file:
                allRequests = json.load(file)
                for privilege in access.privileges:
                    for requestData in allRequests[privilege.name]:
                        print("Request: ", end="")
                        pprint(Request(**requestData))
                        requests.append(Request(**requestData))

            print("Requests: ", end="")
            pprint(requests)

    return Message(type="RequestsList", data=RequestsListMessage(requests=requests))



def processGetMarksList(sessionManager: sm.SessionManager):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True

            try:
                cursor.execute("select id from marks;")
                ids = cursor.fetchall()

                cursor.execute("select column_name from information_schema.columns where table_name=%s", ("marks", ))
                columns: List[str] = list(map(lambda x: x[0], cursor.fetchall()))
            except Exception as e:
                raise DataBaseError()

            marks = []
            for item in ids:
                try:
                    marks.append(markFabric(cursor, item["id"]))
                except Exception as e:
                    print("Warn: can't create mark object with id: ", item["id"], "\nError message: ", e.args)
                    continue

            result = TabledMessage(columns=columns, rows=marks)

            return Message(type="Tabled", data=result)
