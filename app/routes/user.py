
from datetime import datetime, timedelta
from multiprocessing import synchronize
from typing import List
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from typing_extensions import deprecated
from fastapi import FastAPI, Response, status, HTTPException, Depends, utils, APIRouter
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..import models, oauth2
from fastapi import Depends, FastAPI, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import secrets

import logging
from ..config import settings



# from fastapi import FastAPI, Depends, HTTPException, status
# from starlette.responses import JSONResponse
# from db.session import get_db_session
# from db.repository.user import get_user
# from starlette.background import BackgroundTasks
# from pydantic import BaseModel
# from fastapi_mail import FastMail, MessageSchema, MessageType
# from jose import jwt, JWTError
# from passlib.context import CryptContext
# from pydantic import BaseModel


from ..database import SessionLocal, engine, get_db
from ..import schemas, utils
router = APIRouter(
  prefix="/api"
)




@router.post("/register",response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session= Depends(get_db)):
  
    get_user_by_email=db.query(models.User).filter(models.User.email == user.email).first()
    db_user= get_user_by_email
    if db_user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email is alresdy registered")
    
    # hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #return the new post
    return new_user
  
  



@router.get("/users/{id}",response_model=schemas.UserOut)
async def get_user(id,db: Session= Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return user


@router.get("/users",response_model=List[schemas.UserOut])
async def get_post(db: Session= Depends(get_db)):
    posts = db.query(models.User).all()
    print(type(posts))
    return posts
    
    
@router.delete("/users/{id}")
def delete_user(id,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    post_query = db.query(models.User).filter(models.User.id == id)
    deleted_post = post_query.delete(synchronize_session=False)
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn't exist")

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)




conf = ConnectionConfig(
    MAIL_USERNAME = f"{settings.MAIL_USERNAME}",
    MAIL_PASSWORD = f"{settings.MAIL_PASSWORD}",
    MAIL_FROM = f"{settings.MAIL_FROM}",
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = f"{settings.MAIL_SERVER}",
    MAIL_FROM_NAME=f"{settings.MAIL_FROM_NAME}",
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = settings.USE_CREDENTIALS,
    VALIDATE_CERTS = settings.VALIDATE_CERTS,
)


# Initialize FastAPI-Mail instance
fm = FastMail(conf)

# Initialize FastAPI-Mail instance
# fm = FastMail(conf)

class ResetPasswordRequest(BaseModel):
    email: str
    
    
class EmailSchema(BaseModel):
    email: List[EmailStr]



logger = logging.getLogger(__name__)

@router.post("/forgot-password")
async def forgot_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate a unique token for password reset
    reset_token = secrets.token_urlsafe(32)

    # Store the reset token in the database (you may need to add a column for this)
    user.reset_token = reset_token
    print(user.reset_token)
    db.commit()
    
        # Send password reset email
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset</title>
    </head>
    <body>
        <h1>Password Reset</h1>
        <p>Please reset your password by entering a new one below:</p>
        <form action="http://localhost:8000/api/reset-password" method="post">
            <input type="hidden" name="token" value="{reset_token}">
            <label for="new-password">New Password:</label>
            <input type="password" id="new-password" name="new_password" required>
            <br>
            <button type="submit">Reset Password</button>
        </form>
    </body>
    </html>
    """



    # Send password reset email
    message = MessageSchema(
        to=user.email,
        subject="Password Reset Request",
        recipients=[user.email],
        # body=f"Please click here to reset your password: https://example.com/reset-password?token={reset_token}",
        body=html_template.format(reset_token=reset_token),
        subtype="html"  # Specify the subtype here
    )
    
    try:
        await fm.send_message(message)
        logger.info(f"Password reset email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {e}")
        # Roll back the transaction if sending email fails
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to send password reset email")

    return {"message": "Password reset email sent"}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Find the user with the given token
    user = db.query(models.User).filter(models.User.reset_token == request.token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    # Update user's password
    hashed_password = utils.hash(request.new_password)
    user.password = hashed_password
    user.reset_token = None  # Reset the token after password change
    db.commit()

    return {"message": "Password reset successful"}





