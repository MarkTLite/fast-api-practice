"""
User Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from typing import List

from schemas import UserRequest, UserResponse
from db import db_user
from db.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

# Create a user
@router.post("/create", response_model=UserResponse)
def create_user(request: UserRequest, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Get all users
@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.read_all_users(db)


# Get user by id
@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return db_user.read_specific_user(db, id)


# Update user by id
@router.patch("/{id}/update")
def update_specific_user(id: int, request: UserRequest, db: Session = Depends(get_db)):
    return db_user.update_specific_user(db, id, request)


# Delete user by id
@router.delete("/{id}/delete")
def delete_specific_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_specific_user(id, db)
