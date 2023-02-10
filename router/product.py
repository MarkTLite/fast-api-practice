from typing import Optional, List
import time

from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import (
    Response,
    PlainTextResponse,
    HTMLResponse,
)

router = APIRouter(
    prefix="/product",
    tags=["product"],
)

products = ["watch", "phone"]

async def time_consuming_functionality():
    time.sleep(2.0)
    return 'ok'

# Custom Response basic
@router.get("/all")
async def get_all_products():
    await time_consuming_functionality() # Add async without await to let this be bypassed.
    response = Response(
        content=" ".join(products),
        media_type="text/plain",
    )
    response.set_cookie(key="test_cookie", value="Cookie Value")
    return response

@router.get("/withcustomheader")
def with_custom_header(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
):
    return {
        'data': products,
        'custom_header': custom_header,
        'custom_cookie': test_cookie,
    }

@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"example": "<div>Product</div>"}},
            "description": "Returns the HTML for a product",
        },
        404: {
            "content": {"text/plain": {"example": "Object not found"}},
            "description": "Returns text detail of the error",
        },
    },
)
def get_specific_product(id: int):
    if id > len(products):
        return PlainTextResponse(
            content=f"No product of id: {id} found",
            media_type="text/plain",
            status_code=404,
        )
    else:
        product = products[id]
        html = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=html, media_type="text/html", status_code=200)

@router.post('/create')
def create_product(product_name: Optional[str] = Form(...)):
    products.append(product_name)
    return products