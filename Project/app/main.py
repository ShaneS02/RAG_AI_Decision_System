from fastapi import FastAPI, Depends
from .api.analyze import router as analyze_router
from .api.health import router as health_router
from .dependencies import get_rag_service

import logging

logging.basicConfig(level=logging.INFO) #

app = FastAPI(title="Analysis API")

app.include_router(analyze_router, dependencies=[Depends(get_rag_service)])
app.include_router(health_router)