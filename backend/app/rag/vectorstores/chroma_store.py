import chromadb
from pathlib import Path
from typing import Any, Optional, Dict, List

# backend/vectorstores/chromadb  (3 levels up from this file = backend/)
_DEFAULT_PERSIST_DIR = str(Path(__file__).resolve().parents[3] / "vectorstores" / "chromadb")

class ChromaStore:
    def __init__(self, persist_dir: str = _DEFAULT_PERSIST_DIR):
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="customer_support_docs")
    
    def add(self, id: str, text: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None):
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[id],
            metadatas=[metadata] if metadata is not None else None
        )

    def search(self, query_embedding: List[float], n_results: int = 5, where: Optional[Dict[str, Any]] = None) -> Any:
        kwargs: Dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": n_results
        }
        if where:
            kwargs["where"] = where
            
        results = self.collection.query(**kwargs)
        return results

    def update_document_metadata(self, document_id: str, update_dict: Dict[str, Any]):
        result = self.collection.get(where={"document_id": document_id})
        if not result["ids"]:
            return
        
        ids = result["ids"]
        metadatas = result["metadatas"]
        
        if metadatas:
            updated_metadatas = []
            for meta in metadatas:
                if meta is not None:
                    # meta is a Mapping, we create a new dict to update it
                    new_meta = dict(meta)
                    new_meta.update(update_dict)
                    updated_metadatas.append(new_meta)
                else:
                    updated_metadatas.append(update_dict)
            self.collection.update(ids=ids, metadatas=updated_metadatas)