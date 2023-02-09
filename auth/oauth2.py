from typing import Optional
from datetime import timedelta, datetime
from sqlalchemy.orm.session import Session

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from db.database import get_db
from db import db_user

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'd0c0b831c7a0513b8beb1dee9249e165454e3506a88f8067708112bc81ea8394'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate your credentials"
        headers="WWW-Authenticate": "Bearer",
    )
    try:
        payload = jwt.encode(token, SECRET_KEY, ALGORITHM)
        username: str = payload['sub']
        if not username:
            raise cred_exception
    except JWTError:
        raise cred_exception
    
    user = db_user.read_specific_user(db, username)
    if not user:
        raise cred_exception

    return user