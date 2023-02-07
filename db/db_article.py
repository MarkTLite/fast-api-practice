"""
Article Controllers
"""

from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from schemas import ArticleRequest
from db.models import Article


def create_article(request: ArticleRequest, db: Session):
    """Create article"""
    article = Article(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article_by_id(id: int, db: Session):
    """Read article by id"""
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article with {id} not found",
        )

    return article
