import sys
import os

# Add the backend directory to the path so 'app' is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService

chroma_store = ChromaStore()
embedding_service = EmbeddingService()

# Test ChromaStore
chroma_store.add(
    id="1",
    text="How do I reset my password?",
    embedding=embedding_service.embed_text("How do I reset my password?")
)

# Test search
results = chroma_store.search(
    embedding_service.embed_text("How do I reset my password?"),
    n_results=1
)
print(results)
