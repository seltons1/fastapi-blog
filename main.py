from typing import Union, Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(
    title="API de Cursos",
    version="0.2.1",
    description="API para aprender a utilização do FastAPI",
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/blog/unpublished")
def unpublished():
    return {'data': 'All unpublished blogs.'}

@app.get("/blog")
def show(limit = 10, published : bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'Blog List published {limit} from DB {sort}'}
    else:
        return {'data': f'Blog List {limit} from DB {sort}'}

@app.get("/blog/{id}")
def show(id: int):
    return {'data': id}

@app.get("/blog/{id}/comments")
def comments(id):
    return {'data': {'1','2'}}

@app.get("/about")
def about():
    return {'data':{'about page'}}

class Blog(BaseModel):
    title:str
    body:str
    published: Optional[bool]

@app.post("/blog")
def create_blog(blog: Blog):
    #return request
    return {'data' : f'New {blog.title}'}


