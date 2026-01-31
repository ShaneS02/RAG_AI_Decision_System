from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    # Embed a single text string
    def embed_text(self, text: str) -> List[float]:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    # Embed a batch of text strings
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True
        )
        return embeddings.tolist()

