import chromadb
from chromadb.config import Settings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class VectorDB:
    def __init__(self):
        # Updated ChromaDB client initialization
        self.client = chromadb.PersistentClient(path="db")
        self.collection = self.client.get_or_create_collection(
            name="music_knowledge",
            metadata={"hnsw:space": "cosine"}  # Optional: specify distance metric
        )
    
    def add_documents(self, documents: List[str], metadatas: List[dict], ids: List[str]):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results