import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import pandas as pd
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.schema import TextNode
import qdrant_client
from config.config import settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

class QdrantStorage:
    """Handles storing data in Qdrant using LlamaIndex."""
    
    def __init__(self, collection_name: str, url: str = None, in_memory: bool = False):
        """
        Initialize the Qdrant storage.
        
        Args:
            collection_name: Name of the collection to store data in
            url: URL of the Qdrant server (if None, use local or in-memory)
            in_memory: Whether to use in-memory storage (if url is None)
        """
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=settings.embedding_model_name,
        )
        self.collection_name = collection_name
        
        # Initialize Qdrant client
        if url:
            self.client = qdrant_client.QdrantClient(
                url=url, 
                api_key=settings.qdrant_api_key
            )
        else:
            self.client = qdrant_client.QdrantClient(location=":memory:" if in_memory else None)
            
        # Create the vector store
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name
        )
        
    def store_data(self, processed_df: pd.DataFrame, batch_size: int = 100, embedding_column: str = 'embedding') -> VectorStoreIndex:
        """
        Store processed data in Qdrant using LlamaIndex with batch processing.
        
        Args:
            processed_df: DataFrame with processed data and embeddings
            batch_size: Number of items to process in each batch
            embedding_column: Name of the column containing embeddings
            
        Returns:
            LlamaIndex vector store index
        """
        # Create a storage context with the vector store
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        
        # Process DataFrame in batches
        total_rows = len(processed_df)
        for start_idx in range(0, total_rows, batch_size):
            end_idx = min(start_idx + batch_size, total_rows)
            batch_df = processed_df.iloc[start_idx:end_idx]
            
            # Convert batch DataFrame rows to TextNode objects
            nodes = []
            
            for idx, row in batch_df.iterrows():
                # Convert any list-like metadata to strings for compatibility
                metadata = {
                    'title': row['title'],
                    'url': row['url'],
                    'job_levels': json.dumps(row['job_levels']) if isinstance(row['job_levels'], list) else row['job_levels'],
                    'languages': json.dumps(row['languages']) if isinstance(row['languages'], list) else row['languages'],
                    'duration_minutes': row['duration_minutes']
                }
                
                # Create a TextNode with the description as text and metadata
                node = TextNode(
                    text=row['description'],
                    metadata=metadata,
                )
                node=[node]
                if idx == 0:
                    # Create the index with the first batch
                    index = VectorStoreIndex(nodes, storage_context=storage_context)
                else:
                    # Insert additional batches into the existing index
                    index.insert_nodes(node)
        
        return index