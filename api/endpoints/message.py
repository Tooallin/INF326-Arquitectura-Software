from fastapi import APIRouter
from mensajes.services import get_all
from typing import List

router = APIRouter()

@router.get("/search_message")
def SearchMessages(
	q: str | None = Query(None, description="Palabra clave a buscar en los mensajes"),
    author_id: int | None = Query(None, description="Filtrar por ID de autor"),
    thread_id: int | None = Query(None, description="Filtrar por ID de hilo"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
    offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return search_message(q=q, author_id=author_id, thread_id=thread_id, limit=limit, offset=offset)