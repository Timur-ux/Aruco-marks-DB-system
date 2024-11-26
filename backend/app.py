#!venv/bin/python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import src.db.sessionManager as sm
from src.db.requests import processAuth
from src.core.config import DB_CONFIG

import json

app = FastAPI()

# origins from where backend can accept requests
origins = [
        "http://localhost:8080",
        ]

app.add_middleware(
        CORSMiddleware,

        allow_origins=origins,
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
        )

sessionManager = sm.SessionManager(DB_CONFIG)

@app.get("/")
def index():
    response = json.dumps({"data": "Hello vova"})
    return response

@app.get('/api/login')
def auth(access, login, password):
    response = processAuth(sessionManager, access, login, password)
    print(response)

    if("error" in response):
        response = JSONResponse(content={"message": response["error"]}, status_code=int(response["code"]))
    else:
        response = JSONResponse(content=response)

    return response

@app.get('/api/marks')
def getMarksList():
    response = JSONResponse({"data" :  "get marks list result"})
    return response

@app.get('/api/marks/')
def processMark(mark_id):
    response = JSONResponse({"data" : f"get data of mark with id: {mark_id}"})
    return response
