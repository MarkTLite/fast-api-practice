"""
JSON Schema definitions
"""

from pydantic import BaseModel


class UserRequest(BaseModel):
    """Schema For user requests"""

    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response"""

    username: str
    email: str

    class Config:
        orm_mode = True
