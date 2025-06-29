from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from app.pdf_loader import load_pdfs_from_folder
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from app.settings import get_settings
import pinecone
import os

settings = get_settings()

def initialize_pinecone(index_name: str, dimension: int = 384):
    pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENV"])
    if index_name not in pinecone.list_indexes():
        print(f"Creating Pinecone index '{index_name}'...")
        pinecone.create_index(name=index_name, dimension=dimension, metric="cosine")
    else:
        print(f"Pinecone index '{index_name}' already exists.")

def build_or_load_pinecone_index(index_name, embedding_model, docs=None):
    from langchain.vectorstores import Pinecone as LangchainPinecone

    if docs:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        print("Splitting and embedding documents...")
        chunks = splitter.split_documents(docs)
        print(f"Creating Pinecone vector store with {len(chunks)} chunks...")
        return LangchainPinecone.from_documents(chunks, embedding_model, index_name=index_name)
    else:
        print("Loading existing Pinecone index...")
        return LangchainPinecone.from_existing_index(index_name, embedding_model)

def get_rag_chain_with_pinecone():
    index_name = settings.pinecone_index  # e.g., "mobilya1"
    embedding_model = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,  # e.g. 'sentence-transformers/all-MiniLM-L6-v2'
        model_kwargs={"device": "cuda"}
    )

    initialize_pinecone(index_name=index_name, dimension=384)

    if pinecone.describe_index(index_name).status['ready']:
        index_exists = True
    else:
        index_exists = False

    # First-time document indexing (optional)
    docs = None
    if not index_exists or settings.rebuild_index:
        DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", settings.docs_dir))
        docs = load_pdfs_from_folder(DOCS_DIR)
        if not docs:
            raise ValueError("No documents found.")
    
    vectorstore = build_or_load_pinecone_index(index_name=index_name, embedding_model=embedding_model, docs=docs)

    retriever = vectorstore.as_retriever()
    llm = Ollama(model=settings.ollama_model)

    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
