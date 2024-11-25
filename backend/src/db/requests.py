import src.db.sessionManager as sm
from contextlib import closing
from psycopg2.extras import DictCursor

def processAuth(sessionManager: sm.SessionManager, login: str, password: str):
    with closing(sessionManager.createSession()) as session:
        with session.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('select * from locations');
            return cursor.fetchall()
