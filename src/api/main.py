from typing import Annotated
from fastapi import FastAPI, UploadFile, HTTPException
from .models import FileInfo
from pydantic import ValidationError

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile) -> FileInfo:
    filename = file.filename or ""
    total = 0
    chunk = await file.read(1024 * 64)
    while chunk:
        total += len(chunk)
        chunk = await file.read(1024 * 64)

    try:
        info = FileInfo(file=filename, size=total)
    except ValidationError as exc:
        # return pydantic's validation errors as a 400
        raise HTTPException(status_code=400, detail=str(exc.errors()))

    return info