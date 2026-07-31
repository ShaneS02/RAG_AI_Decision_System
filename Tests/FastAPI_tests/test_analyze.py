from fastapi.testclient import TestClient
from Project.app.main import app
from Project.app.dependencies import get_rag_service
from Project.app.schemas.analyze import AnalyzeResponse

"""
Test using a fake RAGService to validate: 
- routing
- request validation
- dependency injection
- response serialization
- schema stability
"""

class FakeRAGService:
    async def analyze(self, text: str) -> AnalyzeResponse:
        return {
            "summary": "Test summary",
            "risks": [
                {
                    "description": "Test risk",
                    "severity": "LOW",
                    "rationale": "Test rationale",
                    "citations": ["test-doc"]
                }
            ],
            "confidence_score": 0.5,
            "confidence_reasoning": "Test confidence"
        }

def override_get_rag_service():
    return FakeRAGService()

#use the fake RAGService above for the test instead of calling real external services
app.dependency_overrides[get_rag_service] = override_get_rag_service


client = TestClient(app)

def test_analyze_response_schema():
    response = client.post(
        "/analyze",
        json={"text": "test input"}
    )

    assert response.status_code == 200

    data = response.json()
    assert set(data.keys()) == {
        "summary",
        "risks",
        "confidence_score",
        "confidence_reasoning",
    }

#to be moved 
def test_upload_invalid_data():
    response = client.post("/uploadFile")

    assert response.status_code == 422