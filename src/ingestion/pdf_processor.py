from contextlib import contextmanager

from base import FileProcessor
import PyPDF2 as pdf

class PdfProcessor(FileProcessor):
    def __init__(self, file):
        super().__init__(file)

    def read_contents(self):
        f = open(self.file, 'rb')
        reader = pdf.PdfReader(f)
        for page in range(len(reader.pages)):
            text = reader.pages[page].extract_text()
            if text and text.strip():
                yield text


if __name__ == '__main__':
    p = PdfProcessor("/Users/santosh.elangovan/PycharmProjects/RAG/pdftrainer/ideas/test.pdf")
    contents = p.read_contents()
    for c in contents:
        print(c)