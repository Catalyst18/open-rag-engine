from typing import Annotated
from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from .models import FileInfo
from pydantic import ValidationError

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile,background_tasks: BackgroundTasks) -> FileInfo:
    total = 0
    chunk = await file.read(1024 * 64)
    while chunk:
        total += len(chunk)
        chunk = await file.read(1024 * 64)
    try:
        info = FileInfo(file=file.filename, size=total)
        background_tasks.add_task(info.save_file, file)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc.errors()))

    return info