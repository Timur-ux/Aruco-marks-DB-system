from contextlib import closing
from psycopg2.extras import DictCursor
import json

from src.core.errors import AccessError, DataBaseError, NotFoundError
from src.db.fabric import accessFabric, userFabric
import src.db.sessionManager as sm

def processAuth(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True
            try:
                user = userFabric(cursor, access, login, password)
            except NotFoundError as e:
                return {"error" : e.args, "code": 404}
            except AccessError as e:
                return {"error" : e.args, "code": 403}
            except DataBaseError as e:
                return {"error" : e.args, "code" : 500}

            return {
                "data": f"{user.login} is logged in successfully",
                "token" : "some access token"
                }


def processRegister(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True
            try:
                user = userFabric(cursor, access, login, password)
            except AccessError as e:
                return {"error" : e.args, "code": 403}
            except DataBaseError as e:
                return {"error" : e.args, "code" : 500}
            except NotFoundError as e:
                try:
                    accessObj = accessFabric(cursor, access)
                except NotFoundError as e:
                    return {"error": "desired access is undefined", "code": 401}
                except DataBaseError as e:
                    return {"error" : e.args, "code" : 500}

                try:
                    cursor.execute(
                        "insert into users(access_level, login, password) values (%s %s %s);"
                        , (accessObj.id, login, password))
                except Exception as e:
                    return {"error" : "database error", "code" : 500}


                return {"data" : f"{login} is registred successfully"}

            # if user exist return error
            return {
                "error": f"{user.login} is already exist",
                "code" : 409
                }

def processGetRequestsList(sessionManager: sm.SessionManager, access_: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True

            try:
                print("Required request list for access: ", access_)
                access = accessFabric(cursor, access_)

            except NotFoundError as e:
                return {"error": e.args, "code": 404}
            except DataBaseError as e:
                return {"error": e.args, "code": 500}
            requests = []

            with open("./requests.json") as file:
                allReuests = json.load(file)
                for privilege in access.privileges:
                    requests.extend(allReuests[privilege.name])

    return {"data" : requests}
