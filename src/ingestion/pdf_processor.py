from contextlib import contextmanager
from typing import Any, Generator

import ollama
from db.chroma import Chroma
from .base import FileProcessor
import PyPDF2 as pdf

class PdfProcessor(FileProcessor):
    def __init__(self, file):
        super().__init__(file)

    def read_contents(self) -> Generator[str, Any, None]:
        f = open(f"/opt/app/src/uploads/{self.file}", 'rb')
        self.log.info(f"Preparing to read file {self.file}")
        reader = pdf.PdfReader(f)
        for page in range(len(reader.pages)):
            text = reader.pages[page].extract_text()
            if text and text.strip():
                yield text

    def parse_chunks(self,chunks:Generator) ->None:
        self.log.info("Preparing to print embeddings")
        chroma = Chroma(collection_name=self.file)
        collection = chroma.create_collection()
        for chunk in chunks:
            ollama_client = ollama.Client(host='http://ollama:11434')
            response = ollama_client.embeddings(model='phi3', prompt=chunk)
            # self.log.info(response)
            embedding_vector = response['embedding']
            chroma.persist_embeddings(collection=collection,chunk_hash=str(hash(chunk)),embeddings=embedding_vector)
            self.log.info(f"Persisted {hash(chunk)}")


    def run(self):
        chunks = self.read_contents()
        self.parse_chunks(chunks=chunks)
    


if __name__ == '__main__':
    p = PdfProcessor("/Users/santosh.elangovan/PycharmProjects/RAG/pdftrainer/ideas/test.pdf")
    contents = p.read_contents()
    for c in contents:
        print(c)