"""
FastAPI application entry point.

ARCHITECTURE:
┌─────────────────┐
│   main.py       │ ← You are here (Application setup)
│  (FastAPI app)  │
└────────┬────────┘
         │
    ┌────┴──────┐
    ▼           ▼
┌─────────┐  ┌──────────────┐
│api/     │  │services/     │
│routes.py│  │search_service│ (Business logic)
│schemas  │  │              │
└─────────┘  └──────────────┘

STARTUP FLOW:
1. FastAPI creates app
2. Include API routes
3. Add CORS middleware
4. On startup: Initialize search service
5. Ready to accept requests!

REQUEST FLOW:
Client (browser/curl)
  ↓ HTTP request
FastAPI app (main.py)
  ↓ Route to POST /search
API routes (api/routes.py)
  ↓ Validate request with Pydantic
  ↓ Call SearchService
Search service (services/search_service.py)
  ↓ Encode query, compute similarities
  ↓ Return results
API routes (format response)
  ↓ HTTP response
Client
"""

import sys
import os
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api import router
from services import initialize_search_service


# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

async def startup_event():
    """
    Called when the application starts up.

    WHAT IT DOES:
    - Initialize the search service
    - Load the embedding model
    - Build the search index
    - Prepare for requests

    WHY NOT IN __init__?
    - Startup tasks should be async
    - Allows FastAPI to do other setup first
    - Errors during startup are properly handled
    """
    print("\n" + "=" * 100)
    print("SEMANTIC SEARCH API - STARTING UP")
    print("=" * 100 + "\n")

    try:
        documents_dir = Path(__file__).parent / "data" / "sample_documents"
        initialize_search_service(str(documents_dir))
        print("=" * 100)
        print("✓ API READY - Listening on http://localhost:8000")
        print("=" * 100 + "\n")
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        raise


async def shutdown_event():
    """
    Called when the application shuts down.

    WHAT IT DOES:
    - Clean up resources
    - Close connections
    - Graceful shutdown
    """
    print("\nShutting down semantic search API...")


# Create lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.

    Modern FastAPI pattern for startup/shutdown.
    """
    # Startup
    await startup_event()
    yield
    # Shutdown
    await shutdown_event()


# ============================================================================
# CREATE FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Semantic Search API",
    description="Local semantic search engine using embeddings",
    version="1.0.0",
    lifespan=lifespan,  # Use lifespan context manager
)


# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

# WHAT IS CORS?
# Cross-Origin Resource Sharing
# Allows requests from different domains/ports
#
# WHY DO WE NEED IT?
# Frontend (Next.js): http://localhost:3000
# Backend (FastAPI): http://localhost:8000
# These are different origins → CORS needed!
#
# WITHOUT CORS:
# Browser blocks request (security)
# Error: "Access to XMLHttpRequest blocked by CORS policy"
#
# WITH CORS:
# Browser allows request
# Frontend can call backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js ports
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ============================================================================
# INCLUDE ROUTES
# ============================================================================

app.include_router(
    router,
    prefix="",  # Routes: /health, /search (no prefix)
    tags=["semantic-search"]
)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint - API information.

    Example:
        curl http://localhost:8000/
    """
    return {
        "service": "Semantic Search API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "search": "POST /search",
            "stats": "GET /search/stats",
            "docs": "GET /docs (Swagger UI)",
            "redoc": "GET /redoc (ReDoc)",
        }
    }


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Run with: python main.py
    # Or: uvicorn main:app --reload

    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,
        reload=True,  # Auto-reload on code changes
    )
