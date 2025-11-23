from functools import cached_property

import chromadb
from chromadb import ClientAPI
from chromadb.types import Collection


class Chroma:
    def __init__(self,collection_name:str,host="chroma",port=8000):
        self.host = host
        self.port = port
        self.collection_name = collection_name


    @cached_property
    def client(self)->ClientAPI:
        chroma_client = chromadb.HttpClient(host=self.host,port=self.port)
        return chroma_client


    def create_collection(self):
        collection = self.client.create_collection(name=self.collection_name)
        return collection

    @staticmethod
    def persist_embeddings(collection:Collection,chunk_hash:str,embeddings:list) -> None:
        collection.add(
            embeddings=embeddings,
            ids=[f"{chunk_hash}"]
        )


if __name__ =='__main__':
    pass



