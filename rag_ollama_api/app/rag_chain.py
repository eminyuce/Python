from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Ollama 
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from app.pdf_loader import load_pdfs_from_folder
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

def build_vector_store(docs, embedding_model, index_path="faiss_index"):
    print("Starting to build vector store...")
    index_file = os.path.join(index_path, "index.faiss")
    
    if not os.path.exists(index_file):
        print(f"FAISS index file not found at {index_file}. Will build new index.")
        if not docs:
            raise ValueError("No documents found to build vector store.")

        if not os.path.exists(index_path):
            print(f"Creating index directory at {index_path}")
            os.makedirs(index_path)

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        print("Splitting documents into chunks...")
        chunks = splitter.split_documents(docs)
        print(f"Split into {len(chunks)} chunks.")

        if not chunks:
            raise ValueError("Text splitter produced no chunks. Check your documents.")

        print("Starting embedding of chunks (this may take a while)...")
        vectorstore = FAISS.from_documents(chunks, embedding_model)
        print("Vector store built successfully!")

        print(f"Saving vector store locally at {index_path} ...")
        vectorstore.save_local(index_path)
        print("Vector store saved successfully.")
    else:
        print(f"FAISS index file found at {index_file}. Loading existing index...")
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        print("Vector store loaded successfully.")

    return vectorstore



def get_rag_chain():
    index_path = "faiss_index"  # your folder path
    embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cuda"}
        )

    # Check if FAISS index exists
    if os.path.exists(index_path) and os.path.exists(os.path.join(index_path, "index.faiss")):
        # Load existing index safely
        vectorstore = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
    else:
        # Load documents and build vector store for first time
        DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "documents"))
        print(f"Loading folder from {DOCS_DIR}")
        docs = load_pdfs_from_folder(DOCS_DIR)
        print(f"Loaded {len(docs)} documents from {DOCS_DIR}")
        if len(docs) == 0:
            raise ValueError(f"No documents loaded from {DOCS_DIR}. Please check the folder path and file contents.")
        vectorstore = build_vector_store(docs, embedding_model)

        # Save the FAISS index for future use
        vectorstore.save_local(index_path)

    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=Ollama(model="llama3.1:8b"), retriever=retriever)
