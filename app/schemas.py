# schemas.py

from numbers import Number
from typing import Optional, Any, Dict
from pydantic import BaseModel, EmailStr,  Field
from typing import Annotated
from datetime import datetime


    
    
    
    
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password: str
    class Config:
        ofrom_attributes = True
        
class UserLogin(BaseModel):
    username:EmailStr
    password: str
    class Config:
        ofrom_attributes = True
        
        
class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    created_at: datetime
    class Config:
        ofrom_attributes = True
        
# class VotesCount(BaseModel):
#     votes:int
#     class Config:
#         ofrom_attributes = True
            
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # likes:List[int] = []
    
    
class PostCreate(PostBase):
  pass


class Post(PostBase):
    id:int
    created_at: datetime
    owner_id:int
    owner: UserOut

    class Config:
        ofrom_attributes = True


class PostOut(Post):
  post:Post
  votes:int
  class Config:
    ofrom_attributes = True
        
        

        
class Token(BaseModel):
    access_token:str
    token:str

    class Config:
        ofrom_attributes = True
        
        
class TokenData(BaseModel):
    id:Optional[int] = None


    class Config:
        ofrom_attributes = True




        
class Vote(BaseModel):
  post_id: int
  dir: Annotated[int, Field(ge=0, le=1)]
