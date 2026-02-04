from Project.rag.database.vector_db import VectorDatabase
from Project.rag.llm.embeddings import EmbeddingService

import pytest

# Test adding chunks to the vector database
def test_add_chunks_increases_index_and_metadata():
    embedding_service = EmbeddingService()
    vector_db = VectorDatabase(embedding_service)

    chunks = [
        {
            "text": "cat", 
            "document_id": "1", 
            "chunk_id": "1", 
            "file_name": "test file", 
            "source": "test", 
            "metadata": {}, 
            "citation": "test", 
            "created_at": "2026-02-02T22:17:45.123456+00:00"
        },
        {
            "text": "dog", 
            "document_id": "2", 
            "chunk_id": "2", 
            "file_name": "test file",
            "source": "test", 
            "metadata": {}, 
            "citation": "test", 
            "created_at": "2026-02-02T22:17:45.123456+00:00"
        },
    ]

    vector_db.add_chunks(chunks)

    # Verify that the index and metadata have been updated correctly
    assert vector_db.index.ntotal == 2
    assert len(vector_db.metadata) == 2

# Test searching functionality
def test_embedding_dimension_matches_index():
    embedding_service = EmbeddingService()
    vector_db = VectorDatabase(embedding_service)

    assert vector_db.index.d == embedding_service.get_embedding_dimension()

# Test semantic search returns relevant chunks
def test_semantic_search_returns_relevant_chunk():
    embedding_service = EmbeddingService()
    vector_db = VectorDatabase(embedding_service)

    chunks = [
        {
            "text": "Cats are small animals", 
            "document_id": "1", 
            "chunk_id": "1",
            "file_name": "test file",
            "source": "test", 
            "metadata": {}, 
            "citation": "test", 
            "created_at": "2026-02-02T22:17:45.123456+00:00"
        },
        {
            "text": "Dogs bark loudly", 
            "document_id": "2", 
            "chunk_id": "2",  
            "file_name": "test file",
            "source": "test", 
            "metadata": {}, 
            "citation": "test", 
            "created_at": "2026-02-02T22:17:45.123456+00:00"
        },
    ]

    vector_db.add_chunks(chunks)

    results, scores = vector_db.search("Cats are small animals", top_k=1)

    print(f"results are: {results} \n ----------------------------")

    assert any("Cats" in chunk["text"] for chunk in results)

# Test that search returns the correct order of results based on similarity
def test_results_sorted_by_similarity():
    embedding_service = EmbeddingService()
    vector_db = VectorDatabase(embedding_service)

    chunks = [
        {
            "text": "machine learning models", 
            "document_id": "1", 
            "chunk_id": "1", 
            "file_name": "test file",
            "source": "test", 
            "metadata": {}, 
            "citation": "test", 
            "created_at": "2026-02-02T22:17:45.123456+00:00"
        },
        {
            "text": "neural networks",
            "document_id": "2", 
            "chunk_id": "2", 
            "file_name": "test file",
            "source": "test", 
            "metadata": {}, 
            "citation": "test", 
            "created_at": "2026-02-02T22:17:45.123456+00:00"
        },
    ]

    vector_db.add_chunks(chunks)

    _, scores = vector_db.search("neural networks", top_k=2, min_similarity=0.0)

    assert scores[0] >= scores[1]

# Test searching in an empty database
def test_search_on_empty_db():
    embedding_service = EmbeddingService()
    vector_db = VectorDatabase(embedding_service)

    results, scores = vector_db.search("anything", top_k=5)

    assert results == []
    assert scores is None or scores.size == 0

# Test adding chunks with missing text raises an error
def test_add_chunks_missing_text_raises():
    embedding_service = EmbeddingService()
    vector_db = VectorDatabase(embedding_service)

    bad_chunks = [{"document_id": "1"}]

    with pytest.raises(ValueError):
        vector_db.add_chunks(bad_chunks)
