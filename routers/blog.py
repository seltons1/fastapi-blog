from fastapi import APIRouter

router = APIRouter()

@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def destroy(id, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@routerapp.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id, request: schemas.Blog, db : Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return {'detail': 'Blog updated'}

@router.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['Blog'])
def all_blogs(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blog'])
def show_blog(id: int, response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog id not found")
    else:
        return blog
