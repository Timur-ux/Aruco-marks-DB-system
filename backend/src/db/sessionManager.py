import psycopg2
from src.core.config import DB_CONFIG

class SessionManager:
    def __init__(self, config):
        self.config = config

    def createSession(self):
        return psycopg2.connect(dbname=self.config["dbname"], user=self.config["user"], password=self.config["password"], host=self.config["host"])

sm = SessionManager(DB_CONFIG)
