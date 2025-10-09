from fastapi import APIRouter
from files.services import svc_getall, svc_getby_id

router = APIRouter()

# Obtener todos los archivos
@router.get("/get_all")
def getall():
	return svc_getall()

# Obtener archivo por id
@router.get("/{id}")
def getby_id(file_id: int):
	return svc_getby_id(file_id=file_id)