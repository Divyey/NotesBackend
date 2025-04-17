from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .base import TimestampMixin
from sqlalchemy.sql import func
from pydantic import BaseModel

class SampleInput(BaseModel):
    value: float

class SampleOutput(BaseModel):
    result: float

'''class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())'''

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    role = Column(String)

'''class Notes(TimestampMixin):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))'''

class Note(Base):
    __tablename__ = "notes"
    note_id = Column(Integer, primary_key=True, index=True) #note_id
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
