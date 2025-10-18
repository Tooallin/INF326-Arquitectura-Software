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
        should_clauses = [
            # 1) Coincidencia principal (todos los términos, alta precisión)
            {
                "multi_match": {
                    "query": q,
                    "fields": ["title^3"],
                    "type": "best_fields",
                    "operator": "and",
                    "fuzziness": "1"  # mínima tolerancia (mejor que AUTO)
                }
            },
            # 2) Autocompletado / frase por prefijo
            {
                "multi_match": {
                    "query": q,
                    "fields": ["title^4"],
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