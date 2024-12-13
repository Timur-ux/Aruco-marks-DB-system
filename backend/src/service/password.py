from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verity_password(plain_password: str, hashed_password: str) -> bool:
    print("plain pass: ", plain_password,"\nhashed pass: ", hashed_password)
    return pwd_context.verify(plain_password, hashed_password)
