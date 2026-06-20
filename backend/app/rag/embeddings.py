# Embeddings configuration and models
# TODO: Configure sentence-transformers or other embedding models

from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_text(self, text: str) -> list[float]:
        try:
            return self.model.encode(text).tolist()
        except Exception as e:
            return []
    
