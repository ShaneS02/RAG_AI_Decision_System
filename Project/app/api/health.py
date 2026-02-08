from fastapi import APIRouter

router = APIRouter()

#ensure the service is alive and reachable
@router.get("/health", tags=["system"])
def health():
    return {"status": "ok"}