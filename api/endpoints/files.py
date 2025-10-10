from typing import Optional
from fastapi import APIRouter, Query
from files.services import svc_getall, svc_searchfiles

router = APIRouter()

# Obtener todos los archivos
@router.get("/get_all")
def getall():
	return svc_getall()

# Buscar un archivo segun parametros
@router.get("/search_files")
def SearchFiles(
	q: Optional[str] = Query(None, description="Palabra clave a buscar en los archivos (nombre o contenido)"),
	thread_id: Optional[int] = Query(None, description="Filtrar por ID de hilo asociado"),
	message_id: Optional[int] = Query(None, description="Filtrar por ID de mensaje asociado"),
	pages_min: Optional[int] = Query(None, ge=1, description="Filtrar por cantidad mínima de páginas"),
	pages_max: Optional[int] = Query(None, ge=1, description="Filtrar por cantidad máxima de páginas"),
	limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
	offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return svc_searchfiles(
		q=q,
		thread_id=thread_id,
		message_id=message_id,
		pages_min=pages_min,
		pages_max=pages_max,
		limit=limit,
		offset=offset
	)