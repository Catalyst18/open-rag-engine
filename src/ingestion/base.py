from abc import ABC, abstractmethod
from common.logs import LoggingMixin


#File Processor (base)

class FileProcessor(ABC, LoggingMixin):

    def __init__(self, file):
        self.file = file
        self.text = None

    @abstractmethod
    def process(self):
        pass

    def chunk_text(self):
        print("Chunking text")

    def vector_embedding(self):
        print("Generating embeddings")

    def save_to_db(self):
        print("Saving to vector DB")

    def run_rag_pipeline(self):
        print("Running RAG pipeline")


#Media Processor 

class MediaProcessor(FileProcessor):

    @abstractmethod
    def transcribe(self):
        pass


#Video Processor

class VideoProcessor(MediaProcessor):

    def process(self):
        self.extract_audio()
        self.transcribe()
        self.rag_flow()

    def extract_audio(self):
        print("Extracting audio from video")

    def transcribe(self):
        print("Transcribing extracted audio")
        self.text = "video transcript text"

    def rag_flow(self):
        self.chunk_text()
        self.vector_embedding()
        self.save_to_db()
        self.run_rag_pipeline()


#Audio Processor

class AudioProcessor(MediaProcessor):

    def process(self):
        self.transcribe()
        self.rag_flow()

    def transcribe(self):
        print("Transcribing audio file")
        self.text = "audio transcript text"

    def rag_flow(self):
        self.chunk_text()
        self.vector_embedding()
        self.save_to_db()
        self.run_rag_pipeline()


#image processor

class ImageProcessor(FileProcessor):

    def process(self):
        self.ocr_extract()
        self.rag_flow()

    def ocr_extract(self):
        print("Extracting text using OCR")
        self.text = "image extracted text"

    def rag_flow(self):
        self.chunk_text()
        self.vector_embedding()
        self.save_to_db()
        self.run_rag_pipeline()