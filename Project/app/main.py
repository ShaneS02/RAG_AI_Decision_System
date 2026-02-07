from fastapi import FastAPI, Depends
from .api.analyze import router as analyze_router
from .services.rag_service import RAGService
from .dependencies import get_rag_service

app = FastAPI(title="Analysis API")

app.include_router(analyze_router, dependencies=[Depends(get_rag_service)])