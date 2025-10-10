from fastapi import APIRouter
from api.endpoints import files, message, threads

api_router = APIRouter()

api_router.include_router(message.router, prefix="/message", tags=["Message"])
api_router.include_router(files.router, prefix="/files", tags=["Files"])
api_router.include_router(threads.router, prefix="/threads", tags=["Threads"])
