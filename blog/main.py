from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List, Union




app = FastAPI()

# Deploy a database
#models.Base.metadata.drop_all(engine)
#models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(**request.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def destroy(id, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id, request: schemas.Blog, db : Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return {'detail': 'Blog updated'}
    
@app.post("/blogDetail", status_code=status.HTTP_201_CREATED, tags=['Details'])
def create(request: schemas.Comments, db : Session = Depends(get_db)):
    new_blog = models.Comments(comment=request.comment, blog_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blogDetail", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowComments], tags=['Details'])
def all_comments(db : Session = Depends(get_db)):
    comments = db.query(model.Comments).all()
    return comments

@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['Blog'])
def all_blogs(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blog'])
def show_blog(id: int, response : Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog id not found")
    else:
        return blog

@app.post('/user', tags=['Users'], status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(username=request.username,email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User, tags=['Users'])
def show_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id not found")
    else:
        return user

@app.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=['Users'])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nobody user is found")
    else:
        return users
'''    
@app.post("/user", status_code=status.HTTP_200_OK, tags=['Users'])
def get_user(request: schemas.User, login: Union[str, None] = None,  db: Session = Depends(get_db)):
    #user = db.query(models.User.username).filter(models.User.username=='seltons1')
    return login
'''













'''
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int, db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = (
            result.scalars().unique().one_or_none()
        )
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail="Usuario não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )'''