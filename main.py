from fastapi import FastAPI, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import timedelta
from routers.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException

from app import schemas, crud, models

from app.hashing import authenticate_user

from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

users = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup")
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=409, detail="Email already registered")
    signedup_user = crud.create_user(db, user_data)
    return signedup_user


@app.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get-users/{user_id}")
def get_users(user_id: int, db: Session = Depends(get_db)):
    users = crud.get_user(user_id=user_id, db=db)
    return users
