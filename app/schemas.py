from pydantic import BaseModel
from datetime import datetime


class PostCreate(BaseModel):
    
    
    title : str 
    content : str
    published : bool 


class Post(BaseModel):
    id: int 
    title : str 
    content : str
    published : bool 
    created_at : datetime

    class config:
        orm_mode = True

    

class User(BaseModel):

    name : str  
    username : str 
    password : str 