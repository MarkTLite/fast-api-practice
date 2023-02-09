from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from schemas import ArticleRequest, ArticleResponse
from db.database import get_db
from db import db_article
from auth.oauth2 import oauth2_schema, get_current_user
from db.models import User

router = APIRouter(
    prefix="/article",
    tags=["article"],
)


@router.post("/create", response_model=ArticleResponse)
def create_article(request: ArticleRequest, db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    """Create Article"""
    return db_article.create_article(request, db)


@router.get("/{id}")  # , response_model=ArticleResponse)
def get_article_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Read article by id"""
    return {
        "data": db_article.get_article_by_id(id, db),
        "user": current_user,
    }
