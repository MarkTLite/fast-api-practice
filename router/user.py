"""
User Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from schemas import UserRequest, UserResponse
from db import db_user
from db.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/create", response_model=UserResponse)
def create_user(request: UserRequest, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)
