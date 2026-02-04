from abc import ABC, abstractmethod
from typing import List

class EmbeddingModel(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass


class GenerationModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass