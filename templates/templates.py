from fastapi import APIRouter, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from schemas import ProductRequest
from custom_log import log

router = APIRouter(
    prefix="/template",
    tags=["template"],
)

templates = Jinja2Templates(directory="templates")


@router.post("/product/{id}", response_class=HTMLResponse)
def get_product_page(
    request: Request,
    product: ProductRequest,
    id: int,
    bt: BackgroundTasks,
):
    bt.add_task(log_template_call, f'Template read for id {id}')
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "title": product.title,
            "id": id,
            "price": product.price,
            "description": product.description,
        },
    )


def log_template_call(msg: str):
    """Made for a background task"""
    log("MyAPI", msg)
