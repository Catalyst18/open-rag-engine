#!/usr/bin/env python
import sys
import chromadb
import ollama


OLLAMA_HOST = "http://localhost:11434"
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
EMBED_MODEL = "nomic-embed-text"
LM_MODEL = "phi3"
TOP_K = 5
MAX_CTX_CHARS = 2000


def get_clients():
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    ollama_client = ollama.Client(host=OLLAMA_HOST)
    return chroma_client, ollama_client


def get_relevant_chunks(chroma_client, ollama_client, collection_name: str, question: str, top_k: int = TOP_K):
    emb = ollama_client.embeddings(
        model=EMBED_MODEL,
        prompt=question,
        options={"num_ctx": 1024},
    )
    query_embedding = emb["embedding"]

    try:
        collection = chroma_client.get_collection(name=collection_name)
    except Exception:
        print(f"[!] No collection found for '{collection_name}'")
        return []

    # 3) Query Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])
    if not documents or not documents[0]:
        return []

    return documents[0]


def build_prompt(question: str, context_chunks):
    context = "\n\n---\n\n".join(context_chunks)
    if len(context) > MAX_CTX_CHARS:
        context = context[:MAX_CTX_CHARS]

    prompt = f"""
        You are a helpful assistant answering questions about a PDF document.
        
        Use ONLY the context below to answer. If the answer is not in the context,
        say you don't know.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """.strip()

    return prompt


def answer_question(ollama_client, question: str, context_chunks):
    if not context_chunks:
        return "I couldn't find any relevant information in the stored chunks."

    prompt = build_prompt(question, context_chunks)

    resp = ollama_client.generate(
        model=LM_MODEL,
        prompt=prompt,
    )

    # ollama python client returns a dict with a 'response' key
    return resp.get("response", "").strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python rag_pdf_cli.py <pdf_filename>")
        print("Example: python rag_pdf_cli.py test.pdf")
        sys.exit(1)

    collection_name = sys.argv[1]  # must match the name used in PdfProcessor (self.file)

    chroma_client, ollama_client = get_clients()
    print(f"🔍 Ready to query PDF collection: {collection_name}")
    print("Type your question, or 'exit' to quit.\n")

    while True:
        try:
            question = input("Q> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        # 1) get relevant chunks
        chunks = get_relevant_chunks(chroma_client, ollama_client, collection_name, question)

        # 2) ask phi3
        answer = answer_question(ollama_client, question, chunks)

        print("\nA> " + answer + "\n")


if __name__ == "__main__":
    main()
