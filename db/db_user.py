"""
Helper Functions for users
"""

from sqlalchemy.orm.session import Session
from schemas import UserRequest
from db.models import DbUser
from db.hash import Hash


def create_user(db: Session, request: UserRequest):
    """Create new user in db and return"""
    new_user = DbUser(
        email=request.email,
        username=request.username,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
