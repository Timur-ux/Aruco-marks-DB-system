from jose import jwt
from datetime import datetime, timedelta
from typing import Dict

SECRET = "auf_secrets_stored_heresdjfvbsdvhsdvuhsdvdjvnjdsfnvndjnvadjnvds"
ALGORITHM = "HS256"

def create_access_token(data: Dict) -> str:
    data_copied = data.copy()
    expired_time = datetime.now() + timedelta(minutes=30) # 30 minutes token's awailable by default
    data_copied.update({"exp": expired_time})
    token = jwt.encode(data_copied, SECRET, ALGORITHM)
    return token
    

