from pathlib import Path
from typing import Any, Generator
import ollama
from db.chroma import Chroma
from .base import MediaProcessor
from faster_whisper import WhisperModel
import ffmpeg


UPLOAD_DIR = Path("/opt/app/src/uploads/")

class VideoProcessor(MediaProcessor):
    def __init__(self, file):
        super().__init__(file)

    def extract_audio(self) -> Path:
        video_path = UPLOAD_DIR / self.file
        audio_path = UPLOAD_DIR / f"{self.file}.mp3"
        self.log.info(f"Extracting audio from {video_path}")
        (
            ffmpeg
            .input(str(video_path))
            .output(str(audio_path), ac=1, ar="16000")
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path

    def transcribe_audio(self, audio_path: Path) -> list[dict]:
        self.log.info(f"Transcribing audio: {audio_path}")
        model = WhisperModel("base")
        segments, _ = model.transcribe(str(audio_path))
        return [{"text": s.text, "start": s.start, "end": s.end} for s in segments]

    def read_contents(self) -> Generator[dict, Any, None]:
        audio_path = self.extract_audio()
        try:
            segments = self.transcribe_audio(audio_path)
            for segment in segments:
                if segment["text"].strip():
                    yield segment
        finally:
            if audio_path.exists():
                audio_path.unlink()

    def parse_chunks(self, chunks: Generator) -> None:
        self.log.info("Persisting video transcript embeddings")
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
        self.log.info("Video processing complete.")