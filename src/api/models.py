from pydantic import BaseModel, field_validator
from .enums import FileTypes


class FileInfo(BaseModel):
    file: str
    size: int

    @property
    def _get_file_type(self) -> str:
        parts = self.file.rsplit('.', 1)
        return parts[1].lower() if len(parts) == 2 else ''

    @field_validator('size')
    def validate_size(cls, size: int) -> int:
        max_bytes = 62145 * 1024
        if size <= max_bytes:
            return size
        raise ValueError(f'file size ({size} bytes) exceeds maximum of {max_bytes} bytes')

    @field_validator('file')
    def validate_file_field(cls, file: str) -> str:
        parts = file.rsplit('.', 1)
        if len(parts) != 2:
            raise ValueError('file must include an extension')
        ext = parts[1].lower()
        allowed = {ft.value for ft in FileTypes}
        if ext in allowed:
            return file
        raise ValueError(f'unsupported file type: {ext}')

    @classmethod
    def validated_supported(cls, file: str) -> str | None:
        parts = file.rsplit('.', 1)
        if len(parts) != 2:
            return None
        ext = parts[1].lower()
        allowed = {ft.value for ft in FileTypes}
        return file if ext in allowed else None



