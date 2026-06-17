import chromadb
from pathlib import Path

# backend/vectorstores/chromadb  (3 levels up from this file = backend/)
_DEFAULT_PERSIST_DIR = str(Path(__file__).resolve().parents[3] / "vectorstores" / "chromadb")

class ChromaStore:
    def __init__(self, persist_dir: str = _DEFAULT_PERSIST_DIR):
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="customer_support_docs")
    
    def add(self, id: str, text: str, embedding: list[float], metadata: dict = None):
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[id],
            metadatas=[metadata] if metadata is not None else None
        )

    def search(self, query_embedding: list[float], n_results: int = 5) -> list[dict]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results