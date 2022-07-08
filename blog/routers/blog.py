from fastapi import APIRouter
from .. import database, schemas, models
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['Blog']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(database.get_db)):
    new_blog = models.Blog(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db : Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db : Session = Depends(database.get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return {'detail': 'Blog updated'}

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all_blogs(db : Session = Depends(database.get_db)):
    return blog.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_blog(id: int, response : Response, db : Session = Depends(database.get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog id not found")
    else:
        return blog
