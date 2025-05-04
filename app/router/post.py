from fastapi import Depends,APIRouter,HTTPException,status,Response
from .. import schemas,models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Post"])

@router.get('/posts',response_model=List[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts 

@router.get('/post/{id}')
def get_post(id : int ,db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post not found with id {id}')
    
    return post



@router.post('/',response_model=schemas.Post)
def create_post(post : schemas.PostCreate,db: Session = Depends(get_db)):
    new_post  = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.put('/{id}')
def update_post(id: int ,post : schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id ==id)
    
    old_post = post_query.first()

    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id = {post.id} not found")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete('/{id}')
def delete_post(id : int,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id = {id} not found')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

