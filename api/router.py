from fastapi import APIRouter
from api.endpoints import files, message

api_router = APIRouter()

api_router.include_router(message.router, prefix="/message", tags=["Message"])
api_router.include_router(files.router, prefix="/files", tags=["Files"])
