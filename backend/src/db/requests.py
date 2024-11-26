import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor

def processAuth(sessionManager: sm.SessionManager, access: str, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            session.autocommit = True

            cursor.execute("select id from access where name = %s;", (access,))
            accesses = cursor.fetchall()
            if(access == []):
                return { "error" : "undefined access", "code" : 404 }
            accessId = accesses[0][0]

            # TODO: Some logic to validate access and login and password
            cursor.execute("select * from users where login = %s and password = %s;", (login, password))
            
            users = cursor.fetchall();
            if(users == []):
                return { "error" : "User not found", "code" : 404 }

            for user in users:
                if(user['access_level'] == accessId):
                    return {
                            "done": f"{login} is logged in successfully",
                            "token" : "some access token"
                            }

            return {"error" : "Access denied", "code" : 403}


            
