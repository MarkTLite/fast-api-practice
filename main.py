import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket

from auth import authentication
from db import models
from db.database import engine
from exceptions import Custom404Exception
from templates import templates
import chat_client
from router import (
    user,
    article,
    blog_get,
    blog_post,
    product,
    files,
    dependencies,
)


app = FastAPI()
app.include_router(authentication.router)
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(user.router)
app.include_router(files.router)
app.include_router(product.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get("/")
async def index():
    return HTMLResponse(content=chat_client.html)


clients = []


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


@app.exception_handler(Custom404Exception)
def custom_404_handler(request: Request, exc: Custom404Exception):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


models.Base.metadata.create_all(engine)
# Sample middleware
@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response


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
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")
