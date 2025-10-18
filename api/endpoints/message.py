from fastapi import APIRouter, Query
from mensajes.services import search_message
from typing import List

router = APIRouter()

@router.get("/search_message")
def SearchMessages(
	q: str | None = Query(None, description="Palabra clave a buscar en los mensajes"),
    author_id: int | None = Query(None, description="Filtrar por ID de autor"),
    thread_id: int | None = Query(None, description="Filtrar por ID de hilo"),
	message_id: int | None = Query(None, description="Filtrar por ID de mensaje"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
    offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return search_message(q=q, author_id=author_id, thread_id=thread_id, message_id=message_id, limit=limit, offset=offset)