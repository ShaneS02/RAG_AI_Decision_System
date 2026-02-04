from sentence_transformers import SentenceTransformer
from typing import List
from .base import EmbeddingModel

class EmbeddingService(EmbeddingModel):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    #get the tokenizer from the model
    def tokenizer(self):
        return self.model.tokenizer

    # Get the dimension of the embeddings produced by the model
    def get_embedding_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

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

