from chromadb.utils import embedding_functions

from chroma import Chroma


def embedding_function():
    return embedding_functions.OllamaEmbeddingFunction(
        url=f"http://localhost:11434/api/embeddings",
        model_name="nomic-embed-text"
    )

query_txt ="""what was his achievements"""
ch = Chroma(collection_name="test.pdf",host="localhost")
collection = ch.client.get_collection(name="test.pdf",embedding_function=embedding_function())
print(collection.name)
result = collection.query(query_texts=query_txt)
print(result.items())
print(result.get('documents')[0])




