from pydantic import BaseModel, Field
from typing import List

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="Text to generate embedding for")

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Query text for vector search")
    k: int = Field(5, ge=1, le=100, description="Number of similar results to return")

class SearchResult(BaseModel):
    text: str
    similarity: float

class SearchResponse(BaseModel):
    results: List[SearchResult]