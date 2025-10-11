from api.models import FileInfo

class TestFileInfo:
    def test_correct_file_type(self):
        file = "sample.pdf"
        f = FileInfo.validated_supported(file=file)
        assert f ==file

    def test_wrong_file_type(self):
        file = "sample.png"
        f= FileInfo.validated_supported(file=file)
        assert f is None


