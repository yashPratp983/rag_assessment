import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
import pandas as pd
from Ingestion.metadat_Extractor import MetadataExtractor

class DataProcessor:
    """Processes assessment data into a structured format."""
    
    def __init__(self, metadata_extractor: MetadataExtractor):
        """
        Initialize the data processor.
        
        Args:
            metadata_extractor: Extractor to use for metadata fields
        """
        self.metadata_extractor = metadata_extractor
        
    def process(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Process assessment data into a structured DataFrame."""
        processed_data = []
        
        for i,item in enumerate(data):
            print(f"Processing item {i+1}/{len(data)}")
            processed_item = {
                'title': item.get('Title', ''),
                'url': item.get('URL', ''),
                'description': item.get('Description', ''),
                'job_levels': self.metadata_extractor.extract_metadata('Job Levels', item.get('Job Levels', '')),
                'languages': self.metadata_extractor.extract_metadata('Languages', item.get('Languages', '')),
                'duration_minutes': self.metadata_extractor.extract_metadata('Assessment Length', item.get('Assessment Length', ''))
            }
            processed_data.append(processed_item)
            
        return pd.DataFrame(processed_data)