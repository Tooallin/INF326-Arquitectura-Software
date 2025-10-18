from canales.mapping import index_name
from elastic_search.connection import get_client
import json

def search_channel(
	q: str | None,
	channel_id: int | None,
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
                "fields": ["title"],
                "fuzziness": "AUTO"
            }
        })
    if channel_id:
        filters.append({"term": {"id": channel_id}})

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
            "id": hit["_source"]["id"],
            "title": hit["_source"]["title"],
            "created_at": hit["_source"]["created_at"],
        }
        for hit in result["hits"]["hits"]
    ]

    return {
        "total": result["hits"]["total"]["value"],
        "results": hits
    }