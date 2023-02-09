"""
Authentication related routes
"""
from sqlalchemy.orm.session import Session

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from db.database import get_db
from auth import oauth2
from db.hash import Hash
from db import models
from exceptions import Custom404Exception

router = APIRouter(tags=["authentication"])


@router.post("/token")
def get_token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.username == request.username).first()
    )
    if not user:
        raise Custom404Exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong username",
        )
    if not Hash.verify(user.password, request.password):
        raise Custom404Exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong Password",
        )

    access_token = oauth2.create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
