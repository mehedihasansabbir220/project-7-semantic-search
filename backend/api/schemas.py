"""
Pydantic schemas for API request/response validation.

Schemas define the structure of data flowing in and out of the API.
Pydantic automatically validates data types and provides useful error messages.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class SearchRequest(BaseModel):
    """
    Schema for POST /search request.

    Attributes:
        query: The search query text
        top_k: Number of results to return (default: 5)
    """
    query: str = Field(..., min_length=1, max_length=1000,
                       description="Search query text")
    top_k: int = Field(default=5, ge=1, le=20,
                      description="Number of results to return")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is machine learning?",
                "top_k": 5
            }
        }


class SearchResult(BaseModel):
    """
    Schema for a single search result.

    Attributes:
        chunk_id: Unique identifier for the chunk
        document_id: Parent document identifier
        score: Cosine similarity score (0.0 to 1.0)
        text: The chunk text (preview, truncated)
        filename: Source filename
    """
    chunk_id: str = Field(..., description="Unique chunk identifier")
    document_id: str = Field(..., description="Parent document ID")
    score: float = Field(..., ge=0.0, le=1.0,
                        description="Similarity score (0.0-1.0)")
    text: str = Field(..., description="Chunk text content")
    filename: str = Field(..., description="Source filename")

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "doc_001_chunk_0005",
                "document_id": "doc_001",
                "score": 0.987,
                "text": "Machine learning is a subset of artificial intelligence...",
                "filename": "machine_learning.txt"
            }
        }


class SearchResponse(BaseModel):
    """
    Schema for POST /search response.

    Attributes:
        query: The original search query
        top_k: Number of results requested
        total_results: Number of results returned (≤ top_k)
        results: List of search results
    """
    query: str = Field(..., description="Original search query")
    top_k: int = Field(..., description="Results requested")
    total_results: int = Field(..., ge=0,
                              description="Results returned")
    results: List[SearchResult] = Field(default_factory=list,
                                       description="List of search results")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is machine learning?",
                "top_k": 5,
                "total_results": 3,
                "results": [
                    {
                        "chunk_id": "doc_001_chunk_0000",
                        "document_id": "doc_001",
                        "score": 0.987,
                        "text": "Machine learning is a subset...",
                        "filename": "machine_learning.txt"
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """
    Schema for GET /health endpoint.

    Attributes:
        status: Server status ("healthy" or "unhealthy")
        model_loaded: Whether the embedding model is loaded
        chunks_indexed: Number of chunks in the index
    """
    status: str = Field(..., description="Health status")
    model_loaded: bool = Field(..., description="Embedding model loaded")
    chunks_indexed: int = Field(..., ge=0, description="Chunks in index")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "chunks_indexed": 57
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema for error responses.

    Attributes:
        error: Error message
        detail: Additional error details (optional)
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "Query must be at least 1 character"
            }
        }
