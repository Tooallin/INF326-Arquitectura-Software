from canales.mapping import index_name
from elastic_search.connection import get_client
import json

def search_channel(
	q: str | None,
	channel_id: int | None,
    owner_id: str | None,
    channel_type: str | None,
    is_active: bool | None,
	limit: int,
	offset: int
):
    es = get_client()

    # 🔍 Construcción del query dinámico
    must_clauses = []
    filters = []

    if q:
        should_clauses = [
            # 1) Coincidencia principal (todos los términos, alta precisión)
            {
                "multi_match": {
                    "query": q,
                    "fields": ["name^3"],
                    "type": "best_fields",
                    "operator": "and",
                    "fuzziness": "1"  # mínima tolerancia (mejor que AUTO)
                }
            },
            # 2) Autocompletado / frase por prefijo
            {
                "multi_match": {
                    "query": q,
                    "fields": ["name^4"],
                    "type": "phrase_prefix"
                }
            }
            # 3) (Opcional) Coincidencia exacta si tienes title.keyword en el mapping
            # ,{ "term": { "title.keyword": q } }
        ]

        must_clauses.append({
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1
            }
        })
    if channel_id:
        filters.append({"term": {"channel_id": channel_id}})
    if owner_id:
        filters.append({"term": {"owner_id": owner_id}})
    if channel_type:
        filters.append({"term": {"channel_type": channel_type}})
    if is_active is not None:
        filters.append({"term": {"is_active": is_active}})

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
            "owner_id": hit["_source"]["owner_id"],
            "name": hit["_source"]["name"],
            "users": hit["_source"].get("users", []),
            "threads": hit["_source"].get("threads", []),
            "channel_type": hit["_source"]["channel_type"],
            "is_active": hit["_source"]["is_active"],
            "created_at": hit["_source"]["created_at"],
            "updated_at": hit["_source"].get("updated_at"),
            "deleted_at": hit["_source"].get("deleted_at"),
        }
        for hit in result["hits"]["hits"]
    ]

    return hits