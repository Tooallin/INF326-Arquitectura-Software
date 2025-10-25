from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz", tags=["health"])
def health_check():
	return {"status": "ok"}

@router.get("/livez", tags=["health"])
def liveness_check():
	return {"status": "alive"}