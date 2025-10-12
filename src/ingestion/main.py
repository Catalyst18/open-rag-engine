import ollama
from pdf_processor import PdfProcessor

if __name__ == "__main__":
    print("executing code")
    f = PdfProcessor("/Users/santosh.elangovan/PycharmProjects/RAG/pdftrainer/ideas/test.pdf")
    chunk_generator = f.read_contents()
    for chunk in chunk_generator:
        response = ollama.embeddings(model='phi3', prompt=chunk)
        print(response)
        embedding_vector = response['embedding']
        print(embedding_vector)
        break