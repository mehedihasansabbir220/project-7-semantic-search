"""API module - HTTP endpoints and request/response schemas."""

from api.routes import router
from api.schemas import SearchRequest, SearchResponse, SearchResult, HealthResponse, ErrorResponse

__all__ = [
    "router",
    "SearchRequest",
    "SearchResponse",
    "SearchResult",
    "HealthResponse",
    "ErrorResponse",
]
