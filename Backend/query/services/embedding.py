"""Embedding service for vector encoding of texts."""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sentence_transformers import SentenceTransformer
from config.config import settings
from transformers import AutoTokenizer, AutoModel
import torch
class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        """Initialize the embedding service with a specified model."""
        self.model_name = settings.embedding_model_name

    def get_embeddings(self,text):
        # Load the tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModel.from_pretrained(self.model_name)
        
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Generate embeddings
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Use the [CLS] token embedding as the sentence embedding
        # (or calculate mean of all token embeddings for better representation)
        embeddings = outputs.last_hidden_state[:, 0, :]
        
        return embeddings