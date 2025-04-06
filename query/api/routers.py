"""API routes for the Assessment Search API."""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter
from query.models.schemas import QueryRequest, QueryResponse, AssessmentResponse
from query.services.embedding import EmbeddingService
from query.services.metadata_extractor import LLMMetadataExtractor
from query.services.vector_store import VectorStoreService
from query.utils.helpers import normalize_job_level, parse_json_or_return_as_list
from config.config import settings
from llama_index.core.vector_stores.types import (
    VectorStoreQuery,
    VectorStoreQueryMode,
)
router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_assessments(request: QueryRequest):
    # """Query assessments with semantic search and metadata filtering."""
    # try:

        metadata_extractor = LLMMetadataExtractor()
        embedding_service = EmbeddingService()
        vector_store_service = VectorStoreService()
        
        # Extract metadata from query if not explicitly provided
        extracted_metadata = {}
        extracted_metadata = metadata_extractor.extract_metadata(request.query)
            
        # Use provided filters or fall back to extracted ones
        job_levels = extracted_metadata.get('job_levels')
        languages = extracted_metadata.get('languages')
        min_duration = extracted_metadata.get('min_duration')
        max_duration = extracted_metadata.get('max_duration')
        
        # Create metadata filters
        metadata_filters = vector_store_service.create_metadata_filters(
            job_levels=job_levels,
            languages=languages,
            min_duration=min_duration,
            max_duration=max_duration
        )
        
        embeddings=embedding_service.get_embeddings(request.query)
        print(embeddings.shape)
        query=VectorStoreQuery(
             query_embedding=embeddings[0],
             query_str=request.query,
            filters=metadata_filters,
            similarity_top_k=settings.top_k,
        )
        # Execute the query
        response = vector_store_service.vector_store.query(
            query=query
        )
        
        # Parse the response nodes and create structured output
        results = []
        
        for node in response.nodes:
            # Parse metadata
            metadata = node.metadata
            job_levels_data = metadata.get("job_levels", "[]")
            languages_data = metadata.get("languages", "[]")
            
            # Parse JSON strings if needed
            job_levels_parsed = parse_json_or_return_as_list(job_levels_data)
            languages_parsed = parse_json_or_return_as_list(languages_data)
            
            # Post-processing for job level matching
            if job_levels and isinstance(job_levels_parsed, list):
                normalized_stored_levels = [normalize_job_level(level) for level in job_levels_parsed]
                normalized_query_levels = [normalize_job_level(level) for level in job_levels]
                
                # Only include results with at least one matching job level
                if not any(query_level in normalized_stored_levels for query_level in normalized_query_levels if query_level):
                    continue
            
            # Create structured result
            result = AssessmentResponse(
                title=metadata.get("title", ""),
                url=metadata.get("url", ""),
                description=node.text,
                job_levels=job_levels_parsed,
                languages=languages_parsed,
                duration_minutes=metadata.get("duration_minutes", 0),
                similarity_score=node.score if hasattr(node, 'score') else 0.0
            )
            results.append(result)
            
        # Return structured response
        return QueryResponse(
            results=results,
            total_results=len(results),
            metadata_extracted={
                "job_levels": job_levels if job_levels else [],
                "languages": languages if languages else [],
                "min_duration": min_duration,
                "max_duration": max_duration
            }
        )
        
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
