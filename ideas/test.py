from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import os

# ✅ 1. Load PDF (use raw string or double slashes for Windows paths)
pdf_path = r"C:\Users\TYSON\Desktop\Rag_pdfreader\introductoryRag\high-intensity-training-the-mike-mentzer-way_compress.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# ✅ 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(documents)

# ✅ 3. Create embeddings and store in Chroma
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma.from_documents(chunks, embedding, persist_directory="chroma_db")

# ✅ 4. Create retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# ✅ 5. Connect to local model via Ollama (ensure Ollama app is running)
# You can use "mistral", "llama3", or "phi3" — whichever is downloaded in Ollama
llm = Ollama(model="llama3")  # Change to "llama3" if you prefer

# ✅ 6. Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# ✅ 7. Ask a question loop
print("\n💬 PDF RAG Chatbot (type 'exit' to quit)")
while True:
    query = input("\nAsk a question: ")
    if query.lower() == "exit":
        print("👋 Goodbye!")
        break

    result = qa_chain.invoke({"query": query})
    answer = result["result"].strip()

    # ✅ Confidence check
    if any(x in answer.lower() for x in ["i don't know", "not sure", "no information"]):
        print("🤖 I don’t know.")
    else:
        print(f"🤖 {answer}")
