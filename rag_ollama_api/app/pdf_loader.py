from langchain.document_loaders import PyPDFLoader
import os

def load_pdfs_from_folder(folder_path: str):
    """
    Load all PDFs from a folder and return a list of LangChain Documents.
    """
    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                for doc in docs:
                    doc.metadata["source"] = filename  # Tag for traceability
                all_docs.extend(docs)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    return all_docs
