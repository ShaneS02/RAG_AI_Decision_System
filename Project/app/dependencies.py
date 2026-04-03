from .services.rag_service import RAGService
from Project import VectorDatabase
from Project import EmbeddingService
from Project import HFLocalGenerationModel

embedding = EmbeddingService()
vector_store = VectorDatabase(embedding_service=embedding)
llm_client = HFLocalGenerationModel()
rag_service = RAGService(vector_store, llm_client)

def get_rag_service() -> RAGService:
    return rag_service