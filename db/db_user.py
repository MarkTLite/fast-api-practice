"""
User Controllers
"""

from sqlalchemy.orm.session import Session
from typing import List
from fastapi import status

from schemas import UserRequest
from db.models import User
from db.hash import Hash
from exceptions import Custom404Exception


def create_user(db: Session, request: UserRequest) -> User:
    """Create new user in db and return"""
    new_user = User(
        email=request.email,
        username=request.username,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def read_all_users(db: Session) -> List[User]:
    """Read All Users in Db and return"""
    return db.query(User).all()


def read_specific_user(db: Session, id: int):
    """Read and return a user by id"""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise Custom404Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with {id} not found",
        )
    return user

def read_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise Custom404Exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User: {username} not found",
        )
    return user

def update_specific_user(db: Session, id: int, request: UserRequest):
    """Update a specific user by id"""
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise Custom404Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with {id} not found",
        )
    user.update(
        {
            User.username: request.username,
            User.email: request.email,
            User.password: Hash.bcrypt(request.password),
        }
    )
    db.commit()
    return "success"


def delete_specific_user(id: int, db: Session):
    """Delete specific user by id"""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise Custom404Exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"USer with {id} not found",
        )

    db.delete(user)
    db.commit()
    return "success"
