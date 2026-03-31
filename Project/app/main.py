from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.analyze import router as analyze_router
from .api.health import router as health_router
from .api.upload import router as upload_router
from .dependencies import get_rag_service

import logging

logging.basicConfig(level=logging.INFO) #


app = FastAPI(title="Analysis API")

# ===== CORS configuration =====
origins = [
    "http://localhost:5173",  # React dev server
    # Add production URL later, e.g. "https://myapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended in prod)
    allow_credentials=True,
    allow_methods=["*"],     # allow GET, POST, etc.
    allow_headers=["*"],     # allow all headers
)
# ===== End CORS config =====

app.include_router(analyze_router, dependencies=[Depends(get_rag_service)])
app.include_router(upload_router, dependencies=[Depends(get_rag_service)])
app.include_router(health_router)
