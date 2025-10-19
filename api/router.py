from fastapi import APIRouter
from api.endpoints import files, message, threads, search, channel

api_router = APIRouter()

api_router.include_router(message.router, prefix="/message", tags=["Message"])
api_router.include_router(files.router, prefix="/files", tags=["Files"])
api_router.include_router(threads.router, prefix="/threads", tags=["Threads"])
#api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(channel.router, prefix="/channel", tags=["Channel"])