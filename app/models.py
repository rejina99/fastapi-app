from pydantic.errors import EmailError
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import DateTime
from database import Base
from sqlalchemy.orm import relationship
from routers.token import ACCESS_TOKEN_EXPIRE_MINUTES


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # usertokens = relationship("UserToken", back_populates="owner")


class UserToken(Base):
    __tablename__ = "alltokens"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    # token =
    created_at = Column(DateTime, default=datetime.utcnow)
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # owner = relationship("User", back_populates="alltokens")
