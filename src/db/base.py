from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self,hostname:str):
        self.hostname = hostname

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

