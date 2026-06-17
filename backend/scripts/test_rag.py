import sys
import os

# Add the backend directory to the path so 'app' is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.rag.vectorstores import ChromaStore
from app.rag.embeddings import EmbeddingService
from app.rag.retriever import Retriever
from app.rag.rag_service import RAGService
from app.services.llm_service import LLMService

embedding_service=EmbeddingService()
chroma_store=ChromaStore()
retriever=Retriever(vectorstore=chroma_store, embedding_service=embedding_service)
rag_service=RAGService(retriever=retriever, llm_service=LLMService())
response=rag_service.answer_question("Can I get a refund after 30 days?")
print(response)