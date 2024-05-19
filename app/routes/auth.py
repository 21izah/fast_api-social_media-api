

from fastapi import HTTPException, Depends, utils, APIRouter, status,Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schemas, utils, oauth2, models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import json
router = APIRouter(
  prefix="/api",
  tags=["Authentication"]
)


@router.post("/login",)
async def login_user(userCredential: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == userCredential.username)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credential')
    if not utils.verifyPassword(userCredential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credential')
      
      
      
      #create token
      #return token
      
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
# @router.post("/login")
# async def login_user(userCredential: schemas.UserLogin, db: Session = Depends(get_db)):
#     user_query = db.query(models.User).filter(models.User.email == userCredential.username)
#     user = user_query.first()
#     if not user:
#         raise HTTPException(status_code=403, detail='Invalid credentials')
#     if not utils.verifyPassword(userCredential.password, user.password):
#         raise HTTPException(status_code=403, detail='Invalid credentials')
    
#     # Create token and return it
#     access_token = oauth2.create_access_token(data={"user_id": user.id})
#     return {"access_token": access_token, "token_type": "bearer"}



