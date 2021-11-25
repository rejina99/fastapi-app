from jose.jws import verify
from passlib.context import CryptContext
from app import crud

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_cxt.hash(password)


def verify(hashed_password, plain_password):
    return pwd_cxt.verify(plain_password, hashed_password)


def authenticate_user(db, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not verify(password, user.hashed_password):
        return False
    return user
