from Project.rag.structured_output.structured_generation import format_context, generate_structured_response
from Project.rag.utils.validators import StructuredResponse
from Project.rag.llm.generation import HFLocalGenerationModel
from unittest.mock import MagicMock
import pytest

def test_format_context_basic():
    chunks = [
        {"citation": "file1#chunk1", "text": "Cats are mammals."},
        {"citation": "file1#chunk2", "text": "They sleep a lot."}
    ]

    expected = "[file1#chunk1]\nCats are mammals.\n\n[file1#chunk2]\nThey sleep a lot."
    result = format_context(chunks)
    assert result == expected

def test_format_context_empty():
    assert format_context([]) == ""


def test_generate_structured_response_success():
    chunks = [{"citation": "file.pdf#chunk1", "text": "Cats produce dander."}]
    fake_llm = MagicMock()
    fake_llm.generate.return_value = """
    {
        "summary": "Cats are mammals",
        "risks": [{"description": "Allergy","severity":"LOW","rationale":"Produces dander","citations":["file.pdf#chunk1"]}],
        "confidence_score": 0.95,
        "confidence_reasoning": "Directly stated in sources"
    }
    """

    response: StructuredResponse = generate_structured_response(chunks, fake_llm)

    assert response.summary == "Cats are mammals"
    assert response.risks[0].description == "Allergy"
    assert response.confidence_score == 0.95

def test_generate_structured_response_invalid_json():
    chunks = [{"citation": "file.pdf#chunk1", "text": "Cats produce dander."}]
    fake_llm = MagicMock()

    fake_llm.generate.return_value = "Not JSON"

    
    with pytest.raises(ValueError):
        generate_structured_response(chunks, fake_llm)

def test_generate_structured_response_invalid_schema():
    chunks = [{"citation": "file.pdf#chunk1", "text": "Cats produce dander."}]
    fake_llm = MagicMock()

    # Missing required fields
    fake_llm.generate.return_value = '{"summary": "Cats are mammals"}'

    with pytest.raises(ValueError):
        generate_structured_response(chunks, fake_llm)
