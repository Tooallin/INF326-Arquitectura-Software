from fastapi import APIRouter
from api.endpoints import message

api_router = APIRouter()

api_router.include_router(message.router, prefix="/message", tags=["Message"])
