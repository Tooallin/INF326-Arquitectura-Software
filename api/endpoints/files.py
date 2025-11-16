from typing import Optional, List
from fastapi import APIRouter, Query
from files.services import svc_searchfiles
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class FileSchema(BaseModel):
	id: str
	filename: str
	mime_type: str
	size: int
	bucket: str
	object_key: str

	message_id: Optional[str] = None
	thread_id: Optional[str] = None
	checksum_sha256: Optional[str] = None

	created_at: datetime
	deleted_at: Optional[datetime] = None

# Buscar un archivo segun parametros
@router.get("/search_files", response_model=List[FileSchema])
def SearchFiles(
	q: Optional[str] = Query(None, description="Palabra clave a buscar en los archivos (nombre o contenido)"),
	file_id: Optional[str] = Query(None, description="Filtrar por ID de hilo asociado"),
	thread_id: Optional[str] = Query(None, description="Filtrar por ID de hilo asociado"),
	message_id: Optional[str] = Query(None, description="Filtrar por ID de mensaje asociado"),
	# pages_min: Optional[int] = Query(None, ge=1, description="Filtrar por cantidad mínima de páginas"),
	# pages_max: Optional[int] = Query(None, ge=1, description="Filtrar por cantidad máxima de páginas"),
	limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados (por defecto 10)"),
	offset: int = Query(0, ge=0, description="Desplazamiento de resultados (paginación)")
):
	return svc_searchfiles(
		q=q,
		file_id=file_id,
		thread_id=thread_id,
		message_id=message_id,
		# pages_min=pages_min,
		# pages_max=pages_max,
		limit=limit,
		offset=offset
	)