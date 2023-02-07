from typing import Optional, List
from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])

# providing a request body in post requests
# does some type validation
class BlogModel(BaseModel):
    title: str
    description: str
    likes: int


@router.post("/new")
def create_blog(blog: BlogModel):
    return blog


# Path params and Query params
@router.post("/new2/{id}")
def create_blog(blog: BlogModel, id: int, version: int):
    return {
        "data": blog,
        "version": version,
        "id": id,
    }


# Add Param Metadata, Str and Num Validators and Multiple values
default_comment_query = Query(
    None,
    title="Comment Id",
    description="The id of the comment",
    alias="Comment ID",
    deprecated=True,
)
default_body_query = Body(..., min_length=10, max_length=50, regex="^[a-z\s]*$")
default_path_query = Path(None, le=40, gt=10)

@router.post("/comment/{id}")
def create_comment(
    blog: BlogModel,
    id: int = default_path_query,
    comment_id: int = default_comment_query,
    body: str = default_body_query,
    v: Optional[List[str]] = Query(["1.0", "1.2", "1.4"]),
):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id,
        "body": body,
        "versions": v,
    }
