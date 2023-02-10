"""
JSON Schema definitions
"""

from pydantic import BaseModel
from typing import List


class UserArticle(BaseModel):
    """Article when in User Response"""

    title: str
    published: bool

    class Config:
        orm_mode = True


class ArticleUser(BaseModel):
    """User when in Article Response"""

    id: int
    username: str

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    """Schema For user JSON request"""

    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """Schema for user JSON response"""

    username: str
    email: str
    id: int
    items: List[UserArticle] = []

    class Config:
        orm_mode = True


class ArticleRequest(BaseModel):
    """Schema for Article JSON request"""

    title: str
    content: str
    published: bool
    creator_id: int


class ArticleResponse(BaseModel):
    """Schema for Article JSON response"""

    title: str
    content: str
    published: bool
    user: ArticleUser

    class Config:
        orm_mode = True

class ProductRequest(BaseModel):
    title: str
    description: str
    price: float