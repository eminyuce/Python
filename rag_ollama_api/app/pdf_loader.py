from langchain.document_loaders import PyPDFLoader
import os

def load_pdfs_from_folder(folder_path: str):
    print(f"Starting to load PDFs from folder: {folder_path}")
    
    all_docs = []
    
    try:
        file_list = os.listdir(folder_path)
        print(f"Found {len(file_list)} files/folders in directory.")
    except Exception as e:
        print(f"Error listing directory {folder_path}: {e}")
        return all_docs
    
    for filename in file_list:
        print(f"Checking file: {filename}")
        if filename.lower().endswith(".pdf"):
            print(f"File {filename} is a PDF. Preparing to load.")
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                print(f"Skipping {filename} because it is not a file.")
                continue
            try:
                print(f"Creating PyPDFLoader for {file_path}")
                loader = PyPDFLoader(file_path)
                print(f"Loading document(s) from {filename}")
                docs = loader.load()
                print(f"Loaded {len(docs)} document chunks/pages from {filename}")
                for doc in docs:
                    doc.metadata["source"] = filename
                all_docs.extend(docs)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
        else:
            print(f"Skipping {filename} because it is not a PDF.")
            
    print(f"Finished loading PDFs. Total documents loaded: {len(all_docs)}")
    return all_docs
