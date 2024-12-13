import psycopg2
import asyncio
import aiopg
from src.core.config import DB_CONFIG

class SessionManager:
    def __init__(self, config):
        self.config = config

    async def createSession(self):
        return aiopg.connect(dbname=self.config["dbname"], user=self.config["user"], password=self.config["password"], host=self.config["host"])

sm = SessionManager(DB_CONFIG)
