import os
import shutil
from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel, field_validator
from .enums import FileTypes


class FileInfo(BaseModel):
    file: str
    size: int

    @property
    def _get_file_type(self) -> str:
        parts = self.file.rsplit('.', 1)
        return parts[1].lower() if len(parts) == 2 else ''

    def _cleanse_file_name(self):
        pass
    # cleanse the file name

    @field_validator('size')
    def validate_size(cls, size: int) -> int:
        max_bytes = 62145 * 1024
        if size <= max_bytes:
            return size
        raise ValueError(f'file size ({size} bytes) exceeds maximum of {max_bytes} bytes')

    @field_validator('file')
    @classmethod
    def validate_file_field(cls, file: str) -> str:
        parts = file.rsplit('.', 1)
        if len(parts) != 2:
            raise ValueError('file must include an extension')
        ext = parts[1].lower()
        allowed = {ft.value for ft in FileTypes}
        if ext in allowed:
            return file
        raise ValueError(f'unsupported file type: {ext}')

    def save_file(self,file:UploadFile,upload_dir='./uploads'):
        Path(upload_dir).mkdir(parents=True, exist_ok=True)
        file_location = os.path.join(upload_dir,self.file)
        with open(file_location,"wb") as file_buffer:
            shutil.copyfileobj(file.file,file_buffer)
        print(f"Copied {file_location}: {self.file}")




