from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.rag_chain import get_rag_chain
from fastapi import HTTPException
from app.settings import get_settings, Settings # Assuming app/settings.py
from contextlib import asynccontextmanager # New import
# You can also access settings directly for app-wide configuration outside of routes
# For example, to configure logging based on settings
import logging

app = FastAPI()
qa_chain = get_rag_chain()
# --- Logging Configuration ---
# Get settings at the module level to configure logging before app initialization
# This ensures logging is set up correctly based on debug mode from the start.
settings = get_settings()

# Set up basic logging based on debug mode (you can expand this)
if settings.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info(f"Starting {settings.app_name} in {settings.app_env} environment.")


# --- Dependency for RAG Chain ---
# Use a dependency for the RAG chain to manage its lifecycle better
# and potentially allow for mocking in tests.
# Using lru_cache for get_rag_chain_instance similar to get_settings()
# ensures the chain is initialized only once.
# Make sure get_rag_chain_instance in app/rag_chain.py returns the chain.
# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for managing application startup and shutdown events.
    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown").
    """
    logger.info("Application startup: Initializing RAG chain...")
    # This call will populate the cache for get_rag_chain_instance()
    # get_rag_chain_instance()
    logger.info("RAG chain initialized successfully.")
    yield # Application yields control here, runs, and then executes code after yield on shutdown
    logger.info("Application shutdown: Performing cleanup (if any)...")
    # Add any cleanup logic here if needed, e.g., closing connections.

# --- FastAPI App Initialization ---
app = FastAPI(
    title=settings.app_name,
    description="A Retrieval-Augmented Generation (RAG) Chatbot API.",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan # Assign the lifespan context manager here
)

# --- Pydantic Models ---
class Question(BaseModel):
    """
    Request model for the /ask endpoint.
    """
    query: str = Field(..., min_length=1, max_length=1000, description="The user's query for the chatbot.")

class AnswerResponse(BaseModel):
    """
    Response model for the /ask endpoint.
    """
    answer: str = Field(..., description="The generated answer from the RAG model.")
    sources: List[str] = Field(default_factory=list, description="List of source document names that contributed to the answer.")

# --- API Endpoints ---
@app.post("/ask", response_model=AnswerResponse, summary="Ask the RAG Chatbot a question")
async def ask_question(
    q: Question
) -> AnswerResponse:
    """
    Processes a user query using the RAG chain to generate an answer
    and identify source documents.

    - **query**: The question you want to ask the chatbot.
    """
    logger.debug(f"Received query: '{q.query}'")

    try:
        logger.debug("Calling RAG chain...")
        # Await the chain if it's an asynchronous call (common for LLM operations)
        # Ensure your get_rag_chain_instance provides an object with an .ainvoke method
        result = qa_chain({"query": q.query})

        logger.debug(f"Raw result from RAG chain: {result}")

        answer_text = result.get("answer", "")
        if not answer_text and "result" in result:
             answer_text = result.get("result", "")

        sources: List[str] = []
        if "source_documents" in result and result["source_documents"]:
            sources = [
                doc.metadata.get("source", "Unknown Source")
                for doc in result["source_documents"]
                if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict)
            ]
            logger.debug(f"Sources identified: {sources}")
        else:
            logger.debug("No source documents found in the chain's result.")

        return AnswerResponse(answer=answer_text, sources=sources)

    except Exception as e:
        logger.error(f"Error processing query '{q.query}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request. Please try again later."
        )




# Example using the settings in a FastAPI route
@app.get("/")
async def read_root(settings: Settings = Depends(get_settings)):
    """
    Returns basic application information based on current settings.
    """
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "debug_mode": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "ollama_model": settings.ollama_model,
        "embedding_model": settings.embedding_model,
        "faiss_index_directory": settings.faiss_index_dir,
        "documents_directory": settings.docs_dir,
        "message": f"Welcome to the {settings.app_name}!"
    }


# --- Running the Application ---
if __name__ == "__main__":
    import uvicorn
    logger.info(f"Uvicorn starting server on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)