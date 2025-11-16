from fastapi import APIRouter, Query
from canales.services import search_channel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class ChannelUser(BaseModel):
    id: UUID
    joined_at: Optional[datetime]  # Elasticsearch epoch_second → datetime

class ChannelSchema(BaseModel):
    id: UUID
    owner_id: Optional[UUID]
    name: Optional[str]

    users: Optional[List[ChannelUser]]  # nested users[]

    channel_type: Optional[str]         # keyword
    is_active: Optional[bool]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True

@router.get("/search_channel", response_model=List[ChannelSchema])
def SearchChannel(
	q: str | None = Query(None, description="Palabra clave a buscar en los mensajes"),
    channel_id: int | None = Query(None, description="Filtrar por ID de canal"),
    owner_id: str | None = Query(None, description="Filtrar por ID de propietario"),
    channel_type: str | None = Query(None, description="Filtrar por tipo de canal"),
    is_active: bool | None = Query(None, description="Filtrar si esta activo el canal"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
    offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return search_channel(q=q, channel_id=channel_id, owner_id=owner_id, channel_type=channel_type, is_active=is_active, limit=limit, offset=offset)