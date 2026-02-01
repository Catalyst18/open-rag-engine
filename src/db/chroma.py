from functools import cached_property

import chromadb
from chromadb.api import ClientAPI
from typing import Any
from chromadb.utils import embedding_functions
from chromadb.api.types import  EmbeddingFunction


class Chroma:
    def __init__(self,collection_name:str,host="chroma",port=8000):
        self.host = host
        self.port = port
        self.collection_name = collection_name

    @cached_property
    def embedding_function(self) -> EmbeddingFunction:
        return embedding_functions.OllamaEmbeddingFunction(
            url=f"http://ollama:11434/api/embeddings",
            model_name="nomic-embed-text"
        )



    @cached_property
    def client(self)->ClientAPI:
        chroma_client = chromadb.HttpClient(host=self.host,port=self.port)
        return chroma_client


    def create_collection(self):
        collection = self.client.get_or_create_collection(
            name=self.collection_name,embedding_function=self.embedding_function
            )
        return collection

    @staticmethod
    def persist_embeddings(collection: Any,chunk_hash:str,embeddings:list,document:str) -> None:
        collection.add(
            embeddings=embeddings,
            documents=[document],
            ids=[f"{chunk_hash}"]
        )


if __name__ =='__main__':
    pass



