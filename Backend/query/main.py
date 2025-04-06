"""Main application module for the Assessment Search API."""
from fastapi import FastAPI
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from query.api.routers import router

# Create FastAPI app
app = FastAPI(title="Assessment Query API")

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,workers=1)