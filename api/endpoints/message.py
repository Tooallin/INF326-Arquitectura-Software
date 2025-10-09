from fastapi import APIRouter
from mensajes.services import get_all
from typing import List

router = APIRouter()

#Crear el mensaje base de una conversacion para un usuario autenticado
@router.get("/get_all/{thread_id}")
def GetAll(thread_id: int):
	return get_all(thread_id=thread_id)