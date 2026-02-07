from fastapi import APIRouter, HTTPException, Depends
from ..schemas.analyze import AnalyzeRequest, AnalyzeResponse
from ..services.rag_service import RAGService
from ..dependencies import get_rag_service  # or wherever it lives

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse, tags=["analysis"])
async def analyze(
    request: AnalyzeRequest,
    rag_service: RAGService = Depends(get_rag_service),
) -> AnalyzeResponse:
    try:
        return await rag_service.analyze(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Analysis failed")