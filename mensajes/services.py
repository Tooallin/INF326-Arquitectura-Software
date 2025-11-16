from mensajes.mapping import index_name
from elastic_search.connection import get_client
import json

def search_message(
	q: str | None,
	user_id: int | None,
	thread_id: int | None,
    message_id: int | None,  # 👈 nuevo parámetro opcional
    type_: str | None,
	limit: int,
	offset: int
):
    es = get_client()

    # 🔍 Construcción del query dinámico
    must_clauses = []
    filters = []

    if q:
        must_clauses.append({
            "multi_match": {
                "query": q,
                "fields": ["content"],
                "fuzziness": "AUTO"
            }
        })
    if user_id:
        filters.append({"term": {"user_id": user_id}})
    if thread_id:
        filters.append({"term": {"thread_id": thread_id}})
    if message_id:
        filters.append({"term": {"id": message_id}})
    if type_:                                    # 👈 coincidencia EXACTA
        filters.append({"term": {"type": type_}}) # type = "text" | "audio" | "file"

    # Si no hay palabra clave ni filtros, devolver todo el índice (limitado)
    if not must_clauses and not filters:
        query = {"match_all": {}}
    else:
        query = {
            "bool": {
                "must": must_clauses if must_clauses else [{"match_all": {}}],
                "filter": filters
            }
        }

    # 🔸 Construir cuerpo completo
    body = {
        "query": query,
        "sort": [{"created_at": {"order": "desc"}}],
        "from": offset,
        "size": limit
    }

    # 🔸 Ejecutar búsqueda
    result = es.search(index=index_name, body=body)

    hits = [
        {
            "id": hit["_id"],
            "content": hit["_source"]["content"],
            "user_id": hit["_source"]["user_id"],
            "thread_id": hit["_source"]["thread_id"],
            "type": hit["_source"]["type"],              # opcional
            "paths": hit["_source"].get("paths"),        # opcional
            # 🗓️ FECHAS
            "created_at": hit["_source"].get("created_at"),
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]

    return hits