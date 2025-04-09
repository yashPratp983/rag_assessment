
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import settings
from Ingestion.ingestion_pipeline import IngestionPipeline

def main():
    api_key = settings.groq_api_key
    
    # Create pipeline
    pipeline = IngestionPipeline(
        api_key=api_key,
        llm_model=settings.llm_model_name,
        embedding_model=settings.embedding_model_name,
        qdrant_collection=settings.qdrant_collection_name,
        qdrant_url= settings.qdrant_url,
        qdrant_in_memory=False  # For testing; use False with proper URL in production
    )
    
    # Run ingestion
    result = pipeline.ingest(r"D:\shl_assessment\Backend\shl_assessments.json")
    
    # Display sample
    processed_data = result["dataframe"]
    print(f"Processed {len(processed_data)} items")
    print(f"Vector index contains {len(result['index'].docstore.docs)} documents")
    


if __name__ == "__main__":
    main()