from contextlib import closing
from psycopg2.extras import DictCursor

from src.core.errors import AccessError, DataBaseError, NotFoundError
from src.db.fabric import accessFabric, userFabric
from src.models.user import User
import src.db.sessionManager as sm

def processAuth(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    try:
        user = userFabric(sessionManager, access, login, password)
    except NotFoundError as e:
        return {"error" : e.args, "code": 404}
    except AccessError as e:
        return {"error" : e.args, "code": 403}
    except DataBaseError as e:
        return {"error" : e.args, "code" : 500}

    return {
        "done": f"{user.login} is logged in successfully",
        "token" : "some access token"
        }


def processRegister(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    try:
        user = userFabric(sessionManager, access, login, password)
    except AccessError as e:
        return {"error" : e.args, "code": 403}
    except DataBaseError as e:
        return {"error" : e.args, "code" : 500}
    except NotFoundError as e:
        # if not found process auth
        with closing(sessionManager.createSession()) as session:
            with session.cursor(cursor_factory=DictCursor) as cursor:
                session.autocommit = True

                try:
                    accessObj = accessFabric(sessionManager, access)
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

                
        return {"done" : f"{login} is registred successfully"}

    return {
        "error": f"{user.login} is already exist",
        "code" : 409
        }


            
            
