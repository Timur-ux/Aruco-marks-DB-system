from src.models.privilege import Privilege
from src.core.errors import AccessError, DataBaseError, NotFoundError
from src.models.access import Access
from src.models.user import User
import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor


def accessFabric(sessionManager: sm.SessionManager, access_: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True

            try:
                cursor.execute("select * from access where name = %s;", (access_,))
            except Exception as e:
                raise DataBaseError("database error")
            accesses = cursor.fetchall()
            if(accesses == []):
                raise NotFoundError("Invalid access")
            print(accesses)
            return Access(id = accesses[0]["id"], name = accesses[0]["name"], privileges=list(map(lambda x: Privilege(id=x), accesses[0]["privileges"])))

def userFabric(sessionManager: sm.SessionManager, access_: str, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True

            access = accessFabric(sessionManager, access_)
            # TODO: Some logic to validate access and login and password
            try:
                cursor.execute("select * from users where login = %s and password = %s;", (login, password))
            except Exception as e:
                raise DataBaseError("database error")
            
            users = cursor.fetchall();
            if(users == []):
                raise NotFoundError("Invalid user login and/or password")

            for user in users:
                if(user['access_level'] == access.id):
                    return User(id=user["id"], login=user["login"], password=password, access=access)

        raise AccessError("Access denied")
