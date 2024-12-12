#! /backuper/venvv/bin/python

from typing import Dict, Optional, List
from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
from datetime import datetime
import os

DB_CONFIG = {
        "dbname": "ArucoService",
        "user": "Raison",
        "password": "qwerty",
        "host": "postgres",
        "container": "postgres"
        }

class DBBackuper:
    def __init__(self, container_name: str, user_name: str, db_name: str):
        self.container_name = container_name
        self.user_name = user_name
        self.db_name = db_name

    def dump(self, suffix: str = "") -> None:
        dump_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "_" + suffix
        command = ["docker", "compose", "exec", self.container_name, "pg_dump", "-U",
                   self.user_name, "-d", self.db_name, "-f", f"/dumps/{dump_name}.sql"]
        subprocess.run(command)

    def load(self, dump_name: str) -> None:
        command = ["docker", "compose", "exec", self.container_name, "psql", "-U",
                   self.user_name, "-d", self.db_name, "-f", f"/dumps/{dump_name}.sql"]
        subprocess.run(command)

    def get_dumps(self) -> List[str]:
        result = []
        for _, _, files in os.walk("../dumps"):
            result.extend(files)

        return result

default_backuper = DBBackuper(DB_CONFIG["container"], DB_CONFIG["user"], DB_CONFIG["dbname"]) 
# origins from where backend can accept requests
origins = [ "*" ]

app = FastAPI(docs_url="/api/docs")
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=['*'],
        allow_headers=['*']
        )

@app.get("/api/create_dump")
def createDump(suffix: str = ""):
    status = {"status": "undefined"}
    try:
        default_backuper.dump(suffix)
        status = {"status": "success"}
    except Exception as e:
        status = {"status": "failed"}

    print("Create dump: ", status)
    return status


@app.get("/api/get_dumps")
def getDumps():
    status: Dict = {"status": "undefined"}
    try:
        status["dumps"] = default_backuper.get_dumps()
        status["status"] = "success"
    except Exception as e:
        status = {"status": "failed"}

    print("get dumps: ", status)
    return status

@app.get("/api/restore_dump")
def restoreDump(dump_id: int):
    status: Dict = {"status": "undefined"}
    try:
        dumps = default_backuper.get_dumps()
        if dump_id in range(len(dumps)):
            default_backuper.load(dumps[dump_id])
        status = {"status": "success"}
    except Exception as e:
        status = {"status": "failed"}

    print("restore dump with id", dump_id, ": ", status)
    return status

