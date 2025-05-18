import cohere
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))
    
    def embed_text(self, text: str) -> List[float]:
        response = self.co.embed(texts=[text], model="embed-english-v3.0", input_type="search_document")
        return response.embeddings[0]
    
    def embed_query(self, text: str) -> List[float]:
        response = self.co.embed(texts=[text], model="embed-english-v3.0", input_type="search_query")
        return response.embeddings[0]