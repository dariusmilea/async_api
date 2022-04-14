from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.database.config import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    auth_level = Column(Integer)
