from sentence_transformers import SentenceTransformer
import numpy as np
from utils.logger import logger

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Loading SentenceTransformer model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> np.ndarray:
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            logger.info(f"Generated embedding for text: {text[:50]}...")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise