
from multiprocessing import synchronize
from typing import List
from typing_extensions import deprecated
from fastapi import FastAPI, Response, status, HTTPException, Depends, utils
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import  models
from .database import SessionLocal, engine, get_db
from . import schemas, utils
from .routes import post, user, auth, votes
from .config import settings



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()




from sqlalchemy.orm import Session

from . import models


# Create tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)
 