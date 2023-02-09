from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from auth import authentication
from db import models
from db.database import engine
from exceptions import Custom404Exception
from router import (
    user,
    article,
    blog_get,
    blog_post,
    product,
    files,
)


app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(files.router)
app.include_router(product.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get("/")
def index():
    return {"message": "Hello world!"}


@app.exception_handler(Custom404Exception)
def custom_404_handler(request: Request, exc: Custom404Exception):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


models.Base.metadata.create_all(engine)

# For CORS Error
origins = ["http://localhost:3000"]  # Usually a react local development
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_headers=["*"],
    allow_methods=["*"],
)

# For Static Files
app.mount('/uploads', StaticFiles(directory='uploads') ,name='uploads')