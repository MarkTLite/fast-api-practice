from fastapi import APIRouter, Depends
from fastapi.requests import Request

router = APIRouter(
    prefix="/dependencies",
    tags=["dependencies"],
)


def convert_headers(request: Request):
    out_headers = []
    for k, v in request.headers.items():
        out_headers.append(f"{k} -- {v}")

    return out_headers


@router.get("")
def get_items(headers=Depends(convert_headers)):
    return {
        "items": ["a", "b", "c"],
        "headers": headers,
    }


class Account:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password


@router.post("/user")
def create_user(
    name: str,
    password: str,
    account: Account = Depends(),
):
    return {
        'name': account.name,
    }
