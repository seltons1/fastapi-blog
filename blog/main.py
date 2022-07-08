from fastapi import FastAPI
from blog.database import engine
from .routers import blog, user, comment

app = FastAPI()

# Deploy a database
#models.Base.metadata.drop_all(engine)
#models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(comment.router)