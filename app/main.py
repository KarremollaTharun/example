from fastapi import FastAPI,Body,Depends,HTTPException,status
from pydantic import BaseModel
from .router import auth, post, user
from .database import engine,Base,get_db
from sqlalchemy.orm import Session
from . import utils,models,schemas


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

