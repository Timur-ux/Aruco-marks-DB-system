import psycopg2
from src.core.config import DB_CONFIG

class SessionManager:
    def __init__(self, config):
        self.config = config

    def createSession(self):
        return psycopg2.connect(**self.config)

sm = SessionManager(DB_CONFIG)
