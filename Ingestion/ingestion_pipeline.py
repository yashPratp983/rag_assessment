import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from typing import Dict, Any, Optional
from Ingestion.metadat_Extractor import MetadataExtractor
from Ingestion.data_processor import DataProcessor
from Ingestion.qdrant__storage import QdrantStorage

class IngestionPipeline:
    """Main pipeline for ingesting assessment data."""
    
    def __init__(self, api_key: str, llm_model: str = "mixtral-8x7b-32768", 
                 embedding_model: str = "all-MiniLM-L6-v2",
                 qdrant_collection: str = "assessments",
                 qdrant_url: str = None,
                 qdrant_in_memory: bool = False):
        """
        Initialize the ingestion pipeline.
        
        Args:
            api_key: API key for Groq
            llm_model: Model name to use for metadata extraction
            embedding_model: Model name to use for generating embeddings
            qdrant_collection: Name of the Qdrant collection
            qdrant_url: URL of the Qdrant server (if None, use local or in-memory)
            qdrant_in_memory: Whether to use in-memory Qdrant (if url is None)
        """
        self.metadata_extractor = MetadataExtractor(api_key, llm_model)
        self.data_processor = DataProcessor(self.metadata_extractor)
        self.qdrant_storage = QdrantStorage(qdrant_collection, qdrant_url, qdrant_in_memory)
        
    def ingest(self, data_path: str, pickle_output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process the data, generate embeddings, and store in Qdrant.
        
        Args:
            data_path: Path to the raw JSON data file
            pickle_output_path: Optional path to save the processed DataFrame
            
        Returns:
            Dictionary with processed DataFrame and LlamaIndex index
        """
        # Load data
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        # Process data
        processed_df = self.data_processor.process(data)
                
        # Save DataFrame if output path is provided
        if pickle_output_path:
            processed_df.to_pickle(pickle_output_path)
            
        # Store in Qdrant
        index = self.qdrant_storage.store_data(processed_df)
        
        return {
            "dataframe": processed_df,
            "index": index
        }