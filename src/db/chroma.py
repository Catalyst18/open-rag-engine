import chromadb

class Chroma:
    def __init__(self,file_name: str,embeddings:list):
        self.file_name = file_name
        self.embeddings = embeddings

    @classmethod
    def create_client(cls,host:str,port:int):
        cls.host = host
        cls.port = port
        chroma_client = chromadb.HttpClient(host=cls.host,port=cls.port)
        return chroma_client

    def persist_embeddings(self):
        pass




if __name__ =='__main__':
    client = Chroma.create_client(host='localhost',port=5000)



