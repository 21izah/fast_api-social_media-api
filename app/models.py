# models.py


from pickle import FALSE
from tkinter import CASCADE
from pydantic import BaseModel

# models.py
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base




    

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE),nullable=False)
    owner = relationship("User")
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String,nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text("now()"))
    reset_token = Column(String, nullable=True)
    
    
    
class Vote(Base):
    __tablename__="votes"
    
    user_id=Column(Integer,ForeignKey("users.id", ondelete=CASCADE),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id", ondelete=CASCADE),primary_key=True)


