from pathlib import Path
from typing import Any, Generator
import ollama
import whisper
from db.chroma import Chroma
from .base import MediaProcessor


UPLOAD_DIR = Path("/opt/app/src/uploads/")

class AudioProcessor(MediaProcessor):
    def __init__(self, file):
        super().__init__(file)

    def extract_audio(self) -> Path:
        # Not neccesary for audio files
        return  Path(UPLOAD_DIR / self.file)

    
    def transcribe_audio(self, audio_path: Path) -> list[dict]:
        self.log.info(f"Transcribing audio: {audio_path}")
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path))
        return result["segments"]

    def read_contents(self) -> Generator[dict, Any, None]:
        audio_path = UPLOAD_DIR / self.file
        segments = self.transcribe_audio(audio_path)
        for segment in segments:
            if segment["text"].strip():
                yield segment

        

    def parse_chunks(self, chunks: Generator) -> None:
        self.log.info("Persisting Audio transcript embeddings")
        chroma = Chroma(collection_name=self.file)
        collection = chroma.create_collection()
        ollama_client = ollama.Client(host='http://ollama:11434') 

        for segment in chunks:
            response = ollama_client.embeddings(
                model='nomic-embed-text',
                prompt=segment["text"],
                options={"num_ctx": 1024}
            )
            chroma.persist_embeddings(  
                collection=collection,
                chunk_hash=str(hash(segment["text"])),
                embeddings=response['embedding'],
                document=segment["text"],
            )

    def run(self):
        chunks = self.read_contents()
        self.parse_chunks(chunks=chunks)
        self.log.info("Audio processing complete.")