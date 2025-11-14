from fastapi import APIRouter, Query
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from mensajes.services import search_message
from typing import Optional, List

router = APIRouter()

class MessageSchema(BaseModel):
    id: UUID
    content: Optional[str]
    user_id: UUID
    thread_id: UUID
    
    type: Optional[str]                   # "text", "audio", "file"
    paths: Optional[List[str]]            # lista opcional de rutas
    
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

@router.get("/search_message", response_model=List[MessageSchema])
def SearchMessages(
	q: str | None = Query(None, description="Palabra clave a buscar en los mensajes"),
    user_id: int | None = Query(None, description="Filtrar por ID de autor"),
    thread_id: int | None = Query(None, description="Filtrar por ID de hilo"),
	message_id: int | None = Query(None, description="Filtrar por ID de mensaje"),
    type_: str | None = Query(None, description="Filtrar por tipo de mensaje: text | audio | file"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
    offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return search_message(q=q, user_id=user_id, thread_id=thread_id, message_id=message_id, type_=type_, limit=limit, offset=offset)