from unittest.mock import Mock

import pytest
from Project.app.services.rag_service import RAGService
from Project.rag.database.vector_db import VectorDatabase
from Project.rag.llm.embeddings import EmbeddingService
from Project.rag.utils.validators import StructuredResponse

import pytest

SAMPLE_PDF = "Tests/RAGService_tests/sample-multilingual-text.pdf"

@pytest.fixture(scope="session")
def embedding_service():
    return EmbeddingService(model_name="all-MiniLM-L6-v2")

@pytest.fixture
def real_vector_store(embedding_service):
    return VectorDatabase(embedding_service=embedding_service)

# success test for uploading a document and indexing it in the vector store
def test_upload_indexes_document(real_vector_store):

    service = RAGService(vector_store=real_vector_store, llm=Mock())
    service.upload(SAMPLE_PDF)

    assert real_vector_store.index.ntotal > 0

# Test success vectore store returns relevant chunks for a query
@pytest.mark.parametrize("query, valid", [
    ("What does the passage say about pursuing wealth?", True),
    ("What are the security requirements?", False),
])
def test_retrieval_returns_relevant_chunk(real_vector_store, query, valid):

    service = RAGService(vector_store=real_vector_store, llm=Mock())
    service.upload(SAMPLE_PDF)

    chunks, scores = real_vector_store.search(query, top_k=3)

    if valid:
        assert len(chunks) > 0
        assert scores[0] > 0
    else:
        assert len(chunks) == 0
        assert scores is None

# test full RAG pipeline
@pytest.mark.asyncio
async def test_full_rag_flow(real_vector_store):

    llm = Mock()
    llm.generate.return_value = """
    {
       "summary": "test",
       "risks": [],
       "confidence_score": 0.9,
       "confidence_reasoning": "good context"
    }
    """

    service = RAGService(vector_store=real_vector_store,llm=llm)
    service.upload(SAMPLE_PDF)

    response = await service.analyze("What does the passage say about pursuing wealth?")

    assert response.summary
    assert response.confidence_score > 0