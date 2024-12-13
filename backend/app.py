#!venv/bin/python
from typing import Optional
from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.service.jwt import get_current_user
from src.models.request import AddNewMarkRequest, AuthRequest, ChangeMarkDataRequest, DeleteMarkRequest, DeleteUserRequest, DumpDBRequest, RestoreDumpRequest
from src.models.message import ErrorMessage
from src.models.user import User
from src.core.errors import BackendError
from src.db.sessionManager import sm as sessionManager
from src.service.requests import RequestProccessor
import asyncio

LOG = True

from devtools import pprint

import json

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

# origins from where backend can accept requests
origins = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "https://localhost:8080",
        "https://127.0.0.1:8080",
        "https://localhost:5000",
        "https://127.0.0.1:5000",
        ]

app.add_middleware(
        CORSMiddleware,

        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
        )

requestProccessor = RequestProccessor(sessionManager)

async def handleRequest(requestFunc, *args, **kwargs):
    try:
        if(LOG):
            print("LOG: args: ", args)
        responseData = await requestFunc(*args, **kwargs)
        if(LOG):
            print("LOG: requestFunc: ", requestFunc, "\nresponse: ", end="")
            pprint(responseData)
    except BackendError as e:
        print("Backend error: ", e.args)
        message: ErrorMessage = e.args[0]
        return JSONResponse(content=message.text, status_code=message.code)

    return responseData.model_dump()
        

# --------------------------
# API PROCESSING
# --------------------------
@app.get("/")
async def index():
    response = json.dumps({"data": "Hello From BACK.... END!!!!!!"})
    return response

@app.post('/api/login')
async def auth(response: Response, user: AuthRequest):
    data = await handleRequest(RequestProccessor.auth, requestProccessor, user.access, user.login, user.password, response)
    pprint(response)
    return data

@app.post('/api/register')
async def register(userData: AuthRequest):
    return await handleRequest(RequestProccessor.register, requestProccessor, userData.access, userData.login, userData.password)

@app.get('/api/marks')
async def getMarks(mark_id: Optional[int] = None, user: User = Depends(get_current_user)):
    if(mark_id is None):
        return await getMarksList(user)
    else:
        return await getMarkData(mark_id, user)

async def getMarksList(user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.getMarksList, requestProccessor, user)

async def getMarkData(mark_id: int, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.getMarkData, requestProccessor, mark_id, user)

@app.get('/api/requests')
async def getListOfRequests(access:str, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.getRequestsList, requestProccessor, access, user)

@app.post("/api/marks")
async def changeMarkData(request: ChangeMarkDataRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.changeMarkData, requestProccessor, request.mark_id, request.parameters, user)

@app.put("/api/marks")
async def addNewMark(request: AddNewMarkRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.addNewMark, requestProccessor, request, user)

@app.delete("/api/marks")
async def deleteMark(request: DeleteMarkRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.deleteMark, requestProccessor, request, user)

@app.get("/api/users")
async def getUsers(user_id: Optional[int] = None, user: User = Depends(get_current_user)):
    if(user_id is None):
        return await handleRequest(RequestProccessor.getUsersInfo, requestProccessor, user)
    return await handleRequest(RequestProccessor.getUserInfo, requestProccessor, user_id, user)

@app.delete("/api/users")
async def deleteUser(request: DeleteUserRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.deleteUser, requestProccessor, request.user_id, user)

@app.get("/api/user_actions")
async def getUsersActions(user_id: Optional[int] = None, user: User = Depends(get_current_user)):
    if(user_id is None):
        return await handleRequest(RequestProccessor.getUsersActions, requestProccessor, user)
    return await handleRequest(RequestProccessor.getUserActions, requestProccessor, user_id, user)

@app.put("/api/users")
async def addUser(request: AuthRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.addUser, requestProccessor, request.access, request.login, request.password, user)

@app.post("/api/db/dump")
async def dumpDB(request: DumpDBRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.createDBDump, requestProccessor, request, user)

@app.get("/api/db/dumps")
async def getDumps(user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.getDBDumps, requestProccessor, user)

@app.post("/api/db/dumps")
async def restoreDump(request: RestoreDumpRequest, user: User = Depends(get_current_user)):
    return await handleRequest(RequestProccessor.restoreDBDums, requestProccessor, request, user)
