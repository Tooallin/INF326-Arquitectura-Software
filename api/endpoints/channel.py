from fastapi import APIRouter, Query
from mensajes.services import search_message
from typing import List

router = APIRouter()

@router.get("/search_channel")
def SearchChannel(
	q: str | None = Query(None, description="Palabra clave a buscar en los mensajes"),
    channel_id: int | None = Query(None, description="Filtrar por ID de canal"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
    offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return search_channel(q=q, channel_id=channel_id, limit=limit, offset=offset)