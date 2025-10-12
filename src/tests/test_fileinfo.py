import pytest

from api.models import FileInfo

class TestFileInfo:
    def test_correct_file_type(self):
        file = "sample.pdf"
        f = FileInfo.validate_file_field(file=file)
        assert f ==file

    def test_wrong_file_type(self):
        file = "sample.png"
        with pytest.raises(ValueError, match="unsupported file type: png"):
            FileInfo.validate_file_field(file=file)

