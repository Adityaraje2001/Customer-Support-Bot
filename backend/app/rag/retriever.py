# RAG Retriever logic
# TODO: Implement similarity search logic querying the vector database
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService
class Retriever:
    def __init__(self,vectorstore:ChromaStore,embedding_service:EmbeddingService):
        self.vectorstore = vectorstore
        self.embedding_service = embedding_service
    
    def retrieve(self, query: str,top_k=5):
        retrieved_documents = []
        query_embedding = self.embedding_service.embed_text(query)
        results = self.vectorstore.search(query_embedding,n_results=top_k)
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, distance in zip(documents, metadatas, distances):
            meta = meta or {}  # guard against None metadata from ChromaDB
            retrieved_documents.append({
                "text": doc,
                "source": meta.get("source"),
                "page": meta.get("page"),
                "chunk": meta.get("chunk"),
                "distance": distance
            })
        return retrieved_documents
 
