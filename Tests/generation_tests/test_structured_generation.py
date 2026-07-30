from Project.rag.structured_output.structured_generation import _format_context
from Project import generate_structured_response
from Project import StructuredResponse
from Project import HFLocalGenerationModel
from unittest.mock import MagicMock
import pytest

def test_format_context_basic():
    chunks = [
        {"citation": "file1#chunk1", "text": "Cats are mammals."},
        {"citation": "file1#chunk2", "text": "They sleep a lot."}
    ]

    expected = (
        "[Source: file1#chunk1]\n"
        "Content: Cats are mammals.\n\n"
        "[Source: file1#chunk2]\n"
        "Content: They sleep a lot."
    )

    result = _format_context(chunks)

    assert result == expected

def test_format_context_empty():
    assert _format_context([]) == ""


def test_generate_structured_response_success():
    chunks = [{"citation": "file.pdf#chunk1", "text": "Cats produce dander."}]
    question = "What are the risks of having cats?"
    fake_llm = MagicMock()
    fake_llm.generate.return_value = """
    {
        "summary": "Cats are mammals",
        "risks": [{"description": "Allergy","severity":"LOW","rationale":"Produces dander","citations":["file.pdf#chunk1"]}],
        "confidence_score": 0.95,
        "confidence_reasoning": "Directly stated in sources"
    }
    """

    response: StructuredResponse = generate_structured_response(chunks, fake_llm, question)

    assert response.summary == "Cats are mammals"
    assert response.risks[0].description == "Allergy"
    assert response.confidence_score == 0.95

def test_generate_structured_response_invalid_json():
    chunks = [{"citation": "file.pdf#chunk1", "text": "Cats produce dander."}]
    question = "What are the risks of having cats?"
    fake_llm = MagicMock()

    fake_llm.generate.return_value = "Not JSON"

    
    with pytest.raises(ValueError):
        generate_structured_response(chunks, fake_llm, question)

def test_generate_structured_response_invalid_schema():
    chunks = [{"citation": "file.pdf#chunk1", "text": "Cats produce dander."}]
    question = "What are the risks of having cats?"
    fake_llm = MagicMock()

    # Missing required fields
    fake_llm.generate.return_value = '{"summary": "Cats are mammals"}'

    with pytest.raises(ValueError):
        generate_structured_response(chunks, fake_llm, question)
