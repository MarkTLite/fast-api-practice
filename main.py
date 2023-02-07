from fastapi import FastAPI

from router import user, article, blog_get, blog_post
from db import models
from db.database import engine


app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get("/")
def index():
    return {"message": "Hello world!"}

@app.exception_handler(IDException)

models.Base.metadata.create_all(engine)
