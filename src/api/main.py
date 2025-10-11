from typing import Annotated
from fastapi import FastAPI, Path, File,UploadFile
from .models import FileInfo
from .enums import FileTypes
from fastapi import HTTPException

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile) -> FileInfo: #mybook.pdf
    if FileInfo.validated_supported(file.filename):
        return FileInfo(file=file.filename,size=file.size)
    else:
        raise HTTPException(status_code=400,detail=f"Unsupported file type {file.filename}/n Only {FileTypes.PDF.value} is supported ")