from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import ollama
from db.chroma import Chroma
from .base import FileProcessor
import PyPDF2 as pdf

UPLOAD_DIR = Path("/opt/app/src/uploads/")

class PdfProcessor(FileProcessor):
    def __init__(self, file):
        super().__init__(file)


    @staticmethod
    def chunk_text(text: str, max_chars: int = 1200):
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunk = ""
        for para in paragraphs:
            # If adding this paragraph would exceed size → yield current chunk
            if len(chunk) + len(para) + 2 > max_chars:
                if chunk:
                    yield chunk
                chunk = para  # start new chunk
            else:
                # Add paragraph to the current chunk
                chunk = para if not chunk else f"{chunk}\n\n{para}"

            # If paragraph itself is too large → hard split
            while len(chunk) > max_chars:
                yield chunk[:max_chars]
                chunk = chunk[max_chars:]

        # yield any leftover content
        if chunk:
            yield chunk

    def read_contents(self) -> Generator[str, Any, None]:
        path = UPLOAD_DIR / self.file
        self.log.info(f"Preparing to read file {path}")

        with path.open("rb") as f:
            reader = pdf.PdfReader(f)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text or not text.strip():
                    continue
                for chunk in self.chunk_text(text):
                    yield chunk

    def parse_chunks(self,chunks:Generator) ->None:
        self.log.info("Preparing to print embeddings")
        chroma = Chroma(collection_name=self.file)
        collection = chroma.create_collection()
        for chunk in chunks:
            ollama_client = ollama.Client(host='http://ollama:11434')
            response = ollama_client.embeddings(model='nomic-embed-text', prompt=chunk,options={"num_ctx": 1024})
            # self.log.info(response)
            embedding_vector = response['embedding']
            chroma.persist_embeddings(
                collection=collection,
                chunk_hash=str(hash(chunk)),
                embeddings=embedding_vector,
                document=chunk
            )


    def run(self):
        chunks = self.read_contents()
        self.parse_chunks(chunks=chunks)
        self.log.info(f"Persisted")
    


if __name__ == '__main__':
    pass