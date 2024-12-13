from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict
from fastapi import Depends, HTTPException, Request, status
from psycopg2.extras import DictCursor

from src.db.fabric import UserFabric
from src.models.token import  TokenPayload
from src.models.user import User

from src.db.sessionManager import sm


SECRET = "auf_secrets_stored_heresdjfvbsdvhsdvuhsdvdjvnjdsfnvndjnvadjnvds"
ALGORITHM = "HS256"


def create_access_token(data: Dict) -> str:
    # 30 minutes token's awailable by default
    expired_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = TokenPayload(data=data, expired=expired_time)
    token = jwt.encode(payload.model_dump(), SECRET, ALGORITHM)
    return token


def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found")
    return token


async def get_current_user(token: str = Depends(get_access_token)) -> User | None:
    try:
        payload = jwt.decode(token, SECRET, ALGORITHM)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    userData = TokenPayload(**payload)
    if userData.expired.timestamp() < datetime.now().timestamp():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is expired")

    async with await sm.createSession() as session:
        async with session.cursor(cursor_factory=DictCursor) as cursor:
            return await UserFabric.byId(cursor, userData.data["user_id"])
