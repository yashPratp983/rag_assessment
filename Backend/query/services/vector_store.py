"""Vector store services for semantic search."""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import qdrant_client
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.vector_stores.types import (
    MetadataFilters, 
    MetadataFilter,
    FilterOperator
)
from config.config import settings
from query.utils.helpers import normalize_job_level

class VectorStoreService:
    """Service for vector database operations."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one vector store connection is created."""
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Qdrant client and vector store."""
        self.client = qdrant_client.QdrantClient(url=settings.qdrant_url,api_key=settings.qdrant_api_key)
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=settings.qdrant_collection_name,
        )
        # self.index = VectorStoreIndex.from_vector_store(self.vector_store)
    
    def create_metadata_filters(self, job_levels=None, languages=None, min_duration=None, max_duration=None):
        """
        Create metadata filters for semantic search.
        
        Args:
            job_levels: List of job level strings to filter by
            languages: List of programming language strings to filter by
            min_duration: Minimum duration in minutes
            max_duration: Maximum duration in minutes
            
        Returns:
            MetadataFilters object or None if no filters are applied
        """
        filters = []
        print({"job_levels":job_levels, "languages":languages, "min_duration":min_duration, "max_duration":max_duration})
        # Job levels filter
        if job_levels and isinstance(job_levels, list) and len(job_levels) > 0:
            normalized_job_levels = [normalize_job_level(level) for level in job_levels if level]
            
            if normalized_job_levels:
                job_level_conditions = []
                
                for level in normalized_job_levels:
                    job_level_conditions.append(
                        MetadataFilter(
                            key="job_levels",
                            operator=FilterOperator.CONTAINS,
                            value=level
                        )
                    )
                
                if len(job_level_conditions) > 1:
                    filters.append(job_level_conditions)
                else:
                    filters.extend(job_level_conditions)
                
        # Languages filter
        if languages and isinstance(languages, list) and len(languages) > 0:
            language_conditions = []
            
            for language in languages:
                if language:  # Skip empty strings
                    language_conditions.append(
                        MetadataFilter(
                            key="languages",
                            operator=FilterOperator.CONTAINS,
                            value=language.lower()
                        )
                    )
            
            if len(language_conditions) > 1:
                filters.append(language_conditions)
            elif len(language_conditions) == 1:
                filters.extend(language_conditions)
        
        # Duration filters
        if min_duration is not None:
            filters.append(
                MetadataFilter(
                    key="duration_minutes",
                    operator=FilterOperator.GTE,
                    value=min_duration
                )
            )
            
        if max_duration is not None:
            filters.append(
                MetadataFilter(
                    key="duration_minutes",
                    operator=FilterOperator.LTE,
                    value=max_duration
                )
            )
        
        # Create metadata filters only if we have filters to apply
        if filters:
            return MetadataFilters(
                filters=filters,
                condition="and"
            )
        return None
    
    