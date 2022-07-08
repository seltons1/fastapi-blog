from fastapi import APIRouter
from .. import database, schemas, models
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union

router = APIRouter(
    prefix='/blogDetail',
    tags=['Detail']
)

@router.post("/blogDetail", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Comments, db : Session = Depends(database.get_db)):
    new_blog = models.Comments(comment=request.comment, blog_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blogDetail", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowComments])
def all_comments(db : Session = Depends(database.get_db)):
    comments = db.query(models.Comments).all()
    return comments
