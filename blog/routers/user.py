from fastapi import APIRouter
from .. import database, schemas, models, hashing
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List, Union

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db : Session = Depends(database.get_db)):
    new_user = models.User(username=request.username,email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def show_user(id: int, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id not found")
    else:
        return user

@router.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser],)
def all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nobody user is found")
    else:
        return users
'''    
@router.post("/user", status_code=status.HTTP_200_OK)
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