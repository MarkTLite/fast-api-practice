"""
Article Controllers
"""

from sqlalchemy.orm.session import Session

from schemas import ArticleRequest
from db.models import Article

def create_article(request: ArticleRequest, db: Session):
    article = Article(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id = request.creator_id,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def get_article_by_id(id: int, db: Session):
    article = db.query(Article).filter(Article.id == id).first()
    # Handlke errors
    return article