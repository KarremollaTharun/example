from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,oauth2,utils



router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with username {user_credentials.username} doesnot exist')
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='incorrect password')
    
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})

    return {"access_token" : access_token, "token_type" : "bearer"}
