import os
import subprocess
from datetime import datetime
from typing import List

from src.core.config import DB_CONFIG


class DBBackuper:
    def __init__(self, container_name: str, user_name: str, db_name: str, password: str):
        self.container_name = container_name
        self.user_name = user_name
        self.db_name = db_name
        self.password = password

    def dump(self, suffix: str = "") -> None:
        dump_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "_" + suffix
        command = ["pg_dump", "--clean", "-f", f"/dumps/{dump_name}.sql"]
        print("Trying to call: ", " ".join(command))
        subprocess.run(command)

    def load(self, dump_name: str) -> None:
        command = ["psql", "-f", f"/dumps/{dump_name}"]
        print("Trying to call: ", " ".join(command))
        subprocess.run(command)

    def get_dumps(self) -> List[str]:
        result = []
        for _, _, files in os.walk("/dumps"):
            result.extend(files)

        return result


default_backuper = DBBackuper(
    DB_CONFIG["container"], DB_CONFIG["user"], DB_CONFIG["dbname"], DB_CONFIG["password"])
