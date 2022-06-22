from pydantic import BaseModel
from typing import Optional, List

class MyBaseModel(BaseModel):
    class Config:
        orm_mode = True

class Blog(MyBaseModel):
    title:str
    body:str
    
class Detail(MyBaseModel):
    title:str
    detail: Optional[str]

class Comments(MyBaseModel):
    comment:str

class ShowComments(MyBaseModel):
    comment:str
    blog: Blog

class ShowBlog(Blog):
    comments : List[Comments] = []
    
class User(MyBaseModel):
    username:str
    email:str
    password:str
    
class ShowUser(MyBaseModel):
    username:str
    email:str
