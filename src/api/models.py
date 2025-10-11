from pydantic import BaseModel,field_validator
from .enums import FileTypes
from fastapi import HTTPException


class FileInfo(BaseModel):
    file: str
    size: float

    @property
    def _get_file_type(self):
        ext = self.file.split('.')[1]
        return ext

    @field_validator('file')
    def validated_supported(cls,file) -> str | None:
        ext = file.split('.')[1]
        if ext in FileTypes:
            return file
        else:
            return None



