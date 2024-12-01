#!venv/bin/python
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.models.request import AuthRequest
from src.models.message import ErrorMessage
from src.core.errors import BackendError, NotFoundError
import src.db.sessionManager as sm
from src.service.requests import processAuth, processGetMarksList, processGetRequestsList, processRegister
from src.core.config import DB_CONFIG

LOG = True

from devtools import pprint

import json

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

# origins from where backend can accept requests
origins = [
        "http://localhost:8080",
        ]

app.add_middleware(
        CORSMiddleware,

        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
        )

sessionManager = sm.SessionManager(DB_CONFIG)

def handleRequest(requestFunc, *args):
    try:
        if(LOG):
            print("LOG: args: ", args)
        response = requestFunc(*args)
        if(LOG):
            print("LOG: requestFunc: ", requestFunc, "\nresponse: ", end="")
            pprint(response)
    except BackendError as e:
        message: ErrorMessage = e.args[0]
        return JSONResponse(content=message.text, status_code=message.code)
    except Exception as e:
        print("Undefined exception: ", e.args, "\nSkipping...")
        message = ErrorMessage(text="Undefined error", code=404)
        return JSONResponse(content=message.text, status_code=message.code)

    response = JSONResponse(content=response.model_dump())
    return response
        
@app.get("/")
def index():
    response = json.dumps({"data": "Hello From BACK.... END!!!!!!"})
    return response

@app.post('/api/login')
def auth(user: AuthRequest):
    return handleRequest(processAuth, sessionManager, user.access, user.login, user.password)

@app.post('/api/register')
def register(user: AuthRequest):
    return handleRequest(processRegister, sessionManager, user.access, user.login, user.password)

@app.get('/api/marks')
def getMarks(mark_id: Optional[int] = None):
    if(mark_id is None):
        return getMarksList()
    else:
        return getMarkData(mark_id)

def getMarksList():
    return handleRequest(processGetMarksList, sessionManager)

def getMarkData(mark_id: int):
    return {} # handleRequest(processGetMarksList) # TODO

@app.get('/api/requests')
def getListOfRequests(access:str):
    return  handleRequest(processGetRequestsList, sessionManager, access)

