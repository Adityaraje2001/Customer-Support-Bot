import sys
import os

# Add the backend directory to the path so 'app' is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.embeddings import EmbeddingService

service = EmbeddingService()

vector = service.embed_text(
    "How do I reset my password?"
)
vector2 = service.embed_text("What is the weather in Mumbai today?")

similarity = service.cosine_similarity(vector, vector2)
print(similarity)
