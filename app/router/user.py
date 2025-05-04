from fastapi import Depends, APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from .. import models,utils,schemas
from ..database import get_db


router = APIRouter(tags=["User"])
@router.get('/')
def get_users(db : Session = Depends(get_db)):
    details = db.query(models.User).all()
    return details
    

@router.get('/{id}')
def get_user(id : int, db : Session = Depends(get_db)):
    details = db.query(models.User).filter(models.User.id == id).first()

    if not details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id = {id} not found')
    return details


@router.post('/users')
def create_user(user : schemas.User,db : Session = Depends(get_db)):
    new_user = models.User(**user.dict())

    username = db.query(models.User).filter(models.User.username == new_user.username).first()

    if username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='email already exist')
    
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


