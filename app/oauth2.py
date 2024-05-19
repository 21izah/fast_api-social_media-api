from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .import schemas, utils, oauth2,models
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
  to_encode= data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def verify_access_token(token:str, credential_exception):
  try:
    payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get("user_id")
    if id is None:
      raise credential_exception
    token_data = schemas.TokenData(id=id)
  except JWTError:
    raise credential_exception
  return token_data
  
# def get_current_user(token:str = Depends(oauth2_schema),db: Session = Depends(get_db)):
#   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"www-Authenticate": "Bearer"})
  
#   return verify_access_token(token,credentials_exception)


def get_current_user(token:str = Depends(oauth2_schema),db: Session = Depends(get_db)):
  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"www-Authenticate": "Bearer"})
  token = verify_access_token(token,credential_exception)
  user = db.query(models.User).filter(models.User.id == token.id).first()
  return user

# def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token_data = verify_access_token(token, credentials_exception)
#     user = db.query(models.User).filter(models.User.email == token_data.email).first()
#     return user

#twilo 
#. recovery code     MUGG899J9W27R9RUT1A9THB7