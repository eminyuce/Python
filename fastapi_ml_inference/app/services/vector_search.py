import faiss
import numpy as np
from utils.logger import logger

class VectorSearch:
    def __init__(self, dimension: int):
        logger.info(f"Initializing Faiss index with dimension: {dimension}")
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance index
        self.texts = []  # Store original texts

    def add(self, embedding: np.ndarray, text: str):
        try:
            self.index.add(embedding.reshape(1, -1).astype(np.float32))
            self.texts.append(text)
            logger.info(f"Added text to index: {text[:50]}...")
        except Exception as e:
            logger.error(f"Error adding to index: {str(e)}")
            raise

    def search(self, query_embedding: np.ndarray, k: int) -> list:
        try:
            distances, indices = self.index.search(query_embedding.reshape(1, -1).astype(np.float32), k)
            results = [
                {"text": self.texts[idx], "similarity": 1 / (1 + dist)}  # Convert L2 distance to similarity
                for idx, dist in zip(indices[0], distances[0])
                if idx < len(self.texts)
            ]
            logger.info(f"Search completed, found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            raise