from mensajes.mapping import index_name
from elastic_search.connection import get_client
import json

def search_message(
	q: str | None,
	author_id: int | None,
	thread_id: int | None,
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
    if author_id:
        filters.append({"term": {"author_id": author_id}})
    if thread_id:
        filters.append({"term": {"thread_id": thread_id}})

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
        "sort": [{"sent_at": {"order": "desc"}}],
        "from": offset,
        "size": limit
    }

    # 🔸 Ejecutar búsqueda
    result = es.search(index=index_name, body=body)

    hits = [
        {
            "id": hit["_source"]["id"],
            "content": hit["_source"]["content"],
            "sent_at": hit["_source"]["sent_at"],
            "author_id": hit["_source"]["author_id"],
            "thread_id": hit["_source"]["thread_id"],
        }
        for hit in result["hits"]["hits"]
    ]

    return {
        "total": result["hits"]["total"]["value"],
        "results": hits
    }