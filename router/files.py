import shutil

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/file",
    tags=["file"],
)


@router.post("/file")
def read_file_in_memory(file: bytes = File(...)):
    """In memory handling of files"""
    content = file.decode(encoding="utf-8")
    lines = content.split("\n")
    return {
        "lines": lines,
    }


@router.post("/uploadfile")
def upload_file(upload_file: UploadFile = File(...)):
    path = f"uploads/{upload_file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        "filename": upload_file.filename,
        "type": upload_file.content_type,
    }

@router.get('/download/{name}', response_class=FileResponse)
def download_file(name: str):
    path = f'uploads/{name}'
    return path