
import sys
import os

# Add the backend directory to the path so 'app' is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService
from app.rag.retriever import Retriever

embedding_service = EmbeddingService()
chroma_store = ChromaStore()

retriever = Retriever(vectorstore=chroma_store, embedding_service=embedding_service)
retrieved_docs = retriever.retrieve(
    "Can I get a refund after 30 days?"
)

print(retrieved_docs)
