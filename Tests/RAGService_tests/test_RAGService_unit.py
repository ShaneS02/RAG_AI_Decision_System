
from unittest.mock import Mock, patch
import pytest
from Project.app.services.rag_service import RAGService
from Project.rag.utils.validators import StructuredResponse

#Verify dependencies are stored correctly.
def test_rag_service_initializes():
    vector_store = Mock()
    llm = Mock()

    service = RAGService(vector_store, llm)

    assert service.vector_store == vector_store
    assert service.llm == llm


#Successful upload calls dependencies correctly
@patch("Project.app.services.rag_service.generate_structured_response")
@patch("Project.app.services.rag_service.TokenManager")
@patch("Project.app.services.rag_service.chunk_text")
@patch("Project.app.services.rag_service.ingestion")
def test_upload_success(mock_ingestion, mock_chunk_text, mock_token_manager, mock_generate_structured_response):
    vector_store = Mock()
    llm = Mock()

    vector_store.embedding_service.tokenizer.return_value = "tokenizer"

    mock_ingestion.return_value = {
        "text": "document text",
        "metadata": {}
    }

    mock_chunk_text.return_value = [
        "chunk1",
        "chunk2"
    ]

    vector_store.prepare_chunks.return_value = [
        {"text": "chunk1"}
    ]

    service = RAGService(vector_store, llm)

    service.upload("test.pdf")

    mock_ingestion.assert_called_once_with("test.pdf")
    mock_chunk_text.assert_called_once()
    vector_store.prepare_chunks.assert_called_once()
    vector_store.add_chunks.assert_called_once_with([{"text": "chunk1"}])

#Upload creates TokenManager correctly
@patch("Project.app.services.rag_service.TokenManager")
@patch("Project.app.services.rag_service.chunk_text")
@patch("Project.app.services.rag_service.ingestion")
def test_upload_creates_token_manager(
    mock_ingestion,
    mock_chunk_text,
    mock_token_manager
):

    vector_store = Mock()

    vector_store.embedding_service.tokenizer.return_value = "tokenizer"

    mock_ingestion.return_value = {
        "text": "hello world"
    }

    service = RAGService(vector_store, Mock())

    service.upload("file.pdf")


    mock_token_manager.assert_called_once_with(
        tokenizer="tokenizer",
        target_tokens=200,
        max_tokens=256
    )

#Upload handles ingestion failure
@patch("Project.app.services.rag_service.ingestion")
def test_upload_ingestion_failure(mock_ingestion):

    vector_store = Mock()
    mock_ingestion.side_effect = ValueError("Unsupported file")
    service = RAGService(vector_store, Mock())


    with pytest.raises(ValueError, match="Unsupported file"):
        service.upload("bad.txt")

#Upload does not add chunks if preparation fails
@patch("Project.app.services.rag_service.ingestion")
def test_upload_prepare_failure(mock_ingestion):

    vector_store = Mock()

    mock_ingestion.return_value = {
        "text": "hello"
    }

    vector_store.prepare_chunks.side_effect = Exception("Embedding failed")
    service = RAGService(vector_store, Mock())


    with pytest.raises(Exception):
        service.upload("file.pdf")


    vector_store.add_chunks.assert_not_called()

# Successful analyze returns structured response
@pytest.mark.asyncio
@patch("Project.app.services.rag_service.TokenManager")
@patch("Project.app.services.rag_service.generate_structured_response")
async def test_analyze_success(mock_generate, mock_token_manager):

    vector_store = Mock()
    vector_store.search.return_value = ([{"text": "relevant chunk"}], [0.9])

    expected_response = StructuredResponse(summary="summary", risks=[], confidence_score=0.9, confidence_reasoning="reasoning")

    mock_generate.return_value = expected_response
    service = RAGService(vector_store, Mock())
    result = await service.analyze("What are the risks?")

    assert result == expected_response
    vector_store.search.assert_called_once_with(query="What are the risks?",top_k=5)

# Analyze fails when no chunks retrieved
@pytest.mark.asyncio
async def test_analyze_no_context():

    vector_store = Mock()
    vector_store.search.return_value = ([], [])
    service = RAGService(vector_store, Mock())

    with pytest.raises(ValueError, match="No relevant context retrieved"):
        await service.analyze("unknown question")

# Analyze does not call LLM when retrieval fails
@pytest.mark.asyncio
@patch("Project.app.services.rag_service.generate_structured_response")
async def test_analyze_no_llm_call(mock_generate):

    vector_store = Mock()
    vector_store.search.return_value = ([], [])
    service = RAGService(vector_store, Mock())


    with pytest.raises(ValueError):
        await service.analyze("question")


    mock_generate.assert_not_called()

# LLM generation failure propagates
@pytest.mark.asyncio
@patch("Project.app.services.rag_service.generate_structured_response")
async def test_analyze_generation_failure(mock_generate):

    vector_store = Mock()
    vector_store.search.return_value = ([{"text": "context"}], [0.8])
    mock_generate.side_effect = Exception("LLM failed")
    service = RAGService(vector_store, Mock())


    with pytest.raises(Exception, match="LLM failed"):
        await service.analyze("question")

# Search failure propagates
@pytest.mark.asyncio
async def test_analyze_search_failure():

    vector_store = Mock()
    vector_store.search.side_effect = Exception("FAISS unavailable")
    service = RAGService(vector_store, Mock())


    with pytest.raises(Exception, match="FAISS unavailable"):
        await service.analyze("query")