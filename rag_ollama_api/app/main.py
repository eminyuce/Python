from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.rag_chain import get_rag_chain
from fastapi import HTTPException

app = FastAPI()
qa_chain = get_rag_chain()

class Question(BaseModel):
    query: str

from fastapi import HTTPException

    
@app.post("/ask")
def ask_question(q: Question):
    print(f"[ask_question] Received query: '{q.query}'")

    # 1) Bad‐request if empty
    if not q.query or q.query.strip() == "":
        print("[ask_question] Empty query received, raising 400 Bad Request")
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 2) Call the chain by passing a dict directly
    print("[ask_question] Calling qa_chain with {'query': …}")
    result = qa_chain({"query": q.query})
    print(f"[ask_question] Raw result from qa_chain(): {result}")

    # 3) Extract answer
    answer_text = result.get("result", "")
    print(f"[ask_question] Answer: {answer_text}")

    # 4) Extract sources if they exist; otherwise return empty list
    if "source_documents" in result and result["source_documents"]:
        sources = [doc.metadata.get("source", "") for doc in result["source_documents"]]
        print(f"[ask_question] Sources: {sources}")
    else:
        print("[ask_question] No source_documents returned; using empty list")
        sources = []

    return {
        "answer": answer_text,
        "sources": sources
    }


@app.get("/")
def root():
    return {"message": "RAG Chatbot API with Ollama is running!"}

if __name__ == "__main__":
    import uvicorn
    # Run server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)