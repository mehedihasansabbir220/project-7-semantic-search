"""
FastAPI routes for the semantic search API.

Routes define HTTP endpoints and handle requests/responses.
Business logic is delegated to SearchService (separation of concerns).

HTTP ENDPOINTS:
- POST /search - Semantic search
- GET /health - Health check
"""

from fastapi import APIRouter, HTTPException
from api.schemas import SearchRequest, SearchResponse, SearchResult, HealthResponse, ErrorResponse
from services.search_service import get_search_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        HealthResponse with service status

    WHAT THIS DOES:
    - Verifies the API is running
    - Checks if embedding model is loaded
    - Reports number of indexed chunks
    - Used by load balancers, monitoring systems

    Example:
        curl http://localhost:8000/health
    """
    service = get_search_service()
    stats = service.get_stats()

    return HealthResponse(
        status="healthy",
        model_loaded=stats["model_loaded"],
        chunks_indexed=stats["chunks_indexed"]
    )


@router.post("/search", response_model=SearchResponse, tags=["Search"])
async def search(request: SearchRequest):
    """
    Semantic search endpoint.

    Takes a query, finds semantically similar chunks,
    returns ranked results with similarity scores.

    REQUEST BODY:
    {
        "query": "What is machine learning?",
        "top_k": 5
    }

    RESPONSE:
    {
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
            },
            ... (up to top_k results)
        ]
    }

    PROCESS:
    1. Validate request (Pydantic does this automatically)
    2. Get search service
    3. Execute search with query and top_k
    4. Format results into response schema
    5. Return to client

    ERRORS:
    - 422: Invalid request (bad query format)
    - 500: Server error (empty index, model not loaded)

    Example:
        curl -X POST http://localhost:8000/search \\
             -H "Content-Type: application/json" \\
             -d '{"query": "machine learning", "top_k": 5}'
    """
    try:
        service = get_search_service()

        # Execute search
        results = service.search(query=request.query, top_k=request.top_k)

        # Format results
        search_results = [
            SearchResult(
                chunk_id=result["chunk_id"],
                document_id=result["document_id"],
                score=result["score"],
                text=result["text"],
                filename=result["filename"]
            )
            for result in results
        ]

        return SearchResponse(
            query=request.query,
            top_k=request.top_k,
            total_results=len(search_results),
            results=search_results
        )

    except ValueError as e:
        # Index empty or model not loaded
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        # Unexpected error
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/stats", tags=["Info"])
async def search_stats():
    """
    Get search service statistics.

    Returns:
        Service metrics and status

    Example:
        curl http://localhost:8000/search/stats
    """
    service = get_search_service()
    return service.get_stats()
