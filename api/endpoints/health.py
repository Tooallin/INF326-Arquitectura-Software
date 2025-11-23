from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
def health_check():
	return {"status": "ok"}

@router.get("/livez")
def liveness_check():
	return {"status": "alive"}