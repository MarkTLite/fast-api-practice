from db.database import Base

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey


class User(Base):
    """User Model"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("Article", back_populates="user")


class Article(Base):
    """Article Model"""

    __tablename__ = "articles"
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="items")
