import psycopg2

class SessionManager:
    def __init__(self, config):
        self.config = config

    def createSession(self):
        return psycopg2.connect(**self.config)

