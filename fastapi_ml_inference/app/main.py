from fastapi import FastAPI, HTTPException
from models import TextInput, SearchQuery, SearchResponse
from services.embedding_service import EmbeddingService
from services.vector_search import VectorSearch
from utils.logger import logger
from utils.settings import get_settings
from contextlib import asynccontextmanager

# Get settings at the module level to configure logging before app initialization
# This ensures logging is set up correctly based on debug mode from the start.
settings = get_settings()
# Initialize services
embedding_service = EmbeddingService()
vector_search = None  # Will be initialized after first embedding

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vector_search
    # Initialize vector search with embedding dimension
    sample_embedding = embedding_service.generate_embedding("sample text")
    vector_search = VectorSearch(dimension=sample_embedding.shape[0])
    logger.info("FastAPI application started")
    
    yield
    # Cleanup here

app = FastAPI(
    title="FastAPI ML Inference Service with Vector Search",
    description="A service for generating text embeddings and performing vector search",
    version="1.0.0",
    lifespan=lifespan 
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/add")
async def add_text(input: TextInput):
    try:
        embedding = embedding_service.generate_embedding(input.text)
        vector_search.add(embedding, input.text)
        return {"message": "Text added successfully"}
    except Exception as e:
        logger.error(f"Error in /add endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
    try:
        query_embedding = embedding_service.generate_embedding(query.query)
        results = vector_search.search(query_embedding, query.k)
        return SearchResponse(results=results)
    except Exception as e:
        logger.error(f"Error in /search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Running the Application ---
if __name__ == "__main__":
    import uvicorn
    logger.info(f"Uvicorn starting server on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)