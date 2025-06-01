from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.rag_chain import get_rag_chain

app = FastAPI()
qa_chain = get_rag_chain()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    result = qa_chain(q.query)
    return {
        "answer": result["result"],
        "sources": [doc.metadata.get("source", "") for doc in result["source_documents"]]
    }

@app.get("/")
def root():
    return {"message": "RAG Chatbot API with Ollama is running!"}
