from abc import ABC, abstractmethod
from common.logs import LoggingMixin


class FileProcessor(ABC,LoggingMixin):
    def __init__(self,file):
        self.file = file

    @abstractmethod
    def read_contents(self):
        pass

    def validate_file(self):
        pass

    def tokenizefile(self):
        pass

    def vector_embedding(self):
        pass

    def save_to_db(self):
        pass







