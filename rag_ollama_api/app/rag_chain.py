import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

from app.settings import get_settings  # Settings loader from app/settings.py
from app.pdf_loader import load_pdfs_from_folder  # Your PDF loader

settings = get_settings()


# -------------------------------
# ✅ Utility: Embedding model setup
# -------------------------------
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cuda"}
    )


# -------------------------------
# ✅ Vectorstore builder and saver
# -------------------------------
def build_vector_store(docs, embedding_model, index_path=settings.faiss_index_dir):
    print("Starting to build vector store...")
    index_file = os.path.join(index_path, "index.faiss")

    if not docs:
        raise ValueError("No documents found to build vector store.")

    if not os.path.exists(index_path):
        os.makedirs(index_path)
        print(f"Created index directory at {index_path}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    print("Splitting documents into chunks...")
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    if not chunks:
        raise ValueError("Text splitter produced no chunks. Check your documents.")

    print("Embedding chunks...")
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    print(f"Saving FAISS index to {index_path} ...")
    vectorstore.save_local(index_path)
    print("Vector store saved successfully.")

    return vectorstore


# -------------------------------
# ✅ One-time index preparation (can be triggered manually or auto)
# -------------------------------
def prepare_faiss_index():
    DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", settings.docs_dir))
    index_path = settings.faiss_index_dir

    print(f"Loading documents from {DOCS_DIR}...")
    docs = load_pdfs_from_folder(DOCS_DIR)

    if not docs:
        raise ValueError(f"No documents found in {DOCS_DIR}")

    embedding_model = get_embedding_model()
    return build_vector_store(docs, embedding_model, index_path)


# -------------------------------
# ✅ Load FAISS vectorstore, or auto-build if missing
# -------------------------------
def load_vectorstore():
    index_path = settings.faiss_index_dir
    index_file = os.path.join(index_path, "index.faiss")

    if os.path.exists(index_file):
        embedding_model = get_embedding_model()
        print(f"Loading FAISS index from {index_path} ...")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        print("Vector store loaded successfully.")
        return vectorstore
    else:
        print("FAISS index not found. Building it now...")
        return prepare_faiss_index()

# -------------------------------
# ✅ RAG Chain creation
# -------------------------------
def get_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()
    llm = Ollama(model=settings.ollama_model)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
