"""Pydantic models for request and response schemas."""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union

class QueryRequest(BaseModel):
    """Schema for assessment query requests."""
    query: str
    
class AssessmentResponse(BaseModel):
    """Schema for individual assessment response items."""
    title: str
    url: str
    description: str
    job_levels: List[str]
    languages: List[str]
    duration_minutes: int
    similarity_score: float

class QueryResponse(BaseModel):
    """Schema for the complete query response."""
    results: List[AssessmentResponse]
    total_results: int
