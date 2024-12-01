#!venv/bin/python
from typing import Optional, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.models.request import AddNewMarkRequest, AuthRequest, ChangeMarkDataRequest, DeleteMarkRequest, DeleteUserRequest
from src.models.mark import Mark
from src.models.message import ErrorMessage, Status, StatusMessage
from src.core.errors import BackendError
import src.db.sessionManager as sm
from src.service.requests import RequestProccessor
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
requestProccessor = RequestProccessor(sessionManager)

def handleRequest(requestFunc, *args):
    try:
        if(LOG):
            print("LOG: args: ", args)
        response = requestFunc(*args)
        if(LOG):
            print("LOG: requestFunc: ", requestFunc, "\nresponse: ", end="")
            pprint(response)
    except BackendError as e:
        print("Backend error: ", e.args)
        message: ErrorMessage = e.args[0]
        return JSONResponse(content=message.text, status_code=message.code)
    except Exception as e:
        print("Undefined exception: ", e.args, "\nSkipping...")
        message = ErrorMessage(text="Undefined error", code=404)
        return JSONResponse(content=message.text, status_code=message.code)

    response = JSONResponse(content=response.model_dump())
    return response
        

# --------------------------
# API PROCESSING
# --------------------------
@app.get("/")
def index():
    response = json.dumps({"data": "Hello From BACK.... END!!!!!!"})
    return response

@app.post('/api/login')
def auth(user: AuthRequest):
    return handleRequest(RequestProccessor.auth, requestProccessor, user.access, user.login, user.password)

@app.post('/api/register')
def register(user: AuthRequest):
    return handleRequest(RequestProccessor.register, requestProccessor, user.access, user.login, user.password)

@app.get('/api/marks')
def getMarks(mark_id: Optional[int] = None):
    if(mark_id is None):
        return getMarksList()
    else:
        return getMarkData(mark_id)

def getMarksList():
    return handleRequest(RequestProccessor.getMarksList, requestProccessor,)

def getMarkData(mark_id: int):
    return handleRequest(RequestProccessor.getMarkData, requestProccessor, mark_id)

@app.get('/api/requests')
def getListOfRequests(access:str):
    return handleRequest(RequestProccessor.getRequestsList, requestProccessor, access)

@app.post("/api/marks")
def changeMarkData(request: ChangeMarkDataRequest):
    return handleRequest(RequestProccessor.changeMarkData, requestProccessor, request.mark_id, request.parameters)

@app.put("/api/marks")
def addNewMark(request: AddNewMarkRequest):
    return handleRequest(RequestProccessor.addNewMark, requestProccessor, request)

@app.delete("/api/marks")
def deleteMark(request: DeleteMarkRequest):
    return handleRequest(RequestProccessor.deleteMark, requestProccessor, request)

@app.get("/api/users")
def getUsers(user_id: Optional[int] = None):
    if(user_id is None):
        return handleRequest(RequestProccessor.getUsersInfo, requestProccessor)
    return handleRequest(RequestProccessor.getUserInfo, requestProccessor, user_id)

@app.delete("/api/users")
def deleteUser(request: DeleteUserRequest):
    return handleRequest(RequestProccessor.deleteUser, requestProccessor, request.user_id)

@app.get("/api/user_actions")
def getUsersActions(user_id: Optional[int] = None):
    if(user_id is None):
        return handleRequest(RequestProccessor.getUsersActions, requestProccessor)
    return handleRequest(RequestProccessor.getUserActions, requestProccessor, user_id)

@app.put("/api/users")
def addUser(request: AuthRequest):
    return handleRequest(RequestProccessor.addUser, requestProccessor, request.access, request.login, request.password)
