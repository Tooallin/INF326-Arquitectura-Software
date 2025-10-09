from fastapi import APIRouter
from typing import List

router = APIRouter()

# Consultar en todos los indices
@router.get("/search")
def search(
    q: str = Query(...),
    channel_id: int | None = Query(None),
    thread_id: int | None = Query(None),
    user_id: int | None = Query(None),
    type: str | None = Query("all"),
    limit: int = Query(10),
    offset: int = Query(0)
):
    es = get_client()

    # Mapear tipos a índices
    index_map = {
        "message": "messages",
        "thread": "threads",
        "file": "files"
    }

    # Determinar índices
    if type == "all":
        indices = list(index_map.values())
    else:
        indices = [index_map.get(type, "messages")]

    # === 🧩 Fase 1: buscar hilos si se filtra por canal ===
    thread_ids = []
    if channel_id:
        threads_query = {
            "query": {"term": {"channel_id": channel_id}},
            "_source": False,
            "size": 1000  # ajustar según cantidad
        }
        threads_result = es.search(index="threads", body=threads_query)
        thread_ids = [hit["_id"] for hit in threads_result["hits"]["hits"]]

        # Si no hay hilos, no seguimos
        if not thread_ids:
            return {"results": [], "total": 0}

    # === 🧩 Fase 2: búsqueda principal ===
    filters = []
    if thread_id:
        filters.append({"term": {"thread_id": thread_id}})
    if user_id:
        filters.append({"term": {"user_id": user_id}})
    if thread_ids:
        filters.append({"terms": {"thread_id": thread_ids}})

    query = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": q,
                        "fields": ["content", "title", "name", "description"],
                        "fuzziness": "AUTO"
                    }}
                ],
                "filter": filters
            }
        },
        "from": offset,
        "size": limit
    }

    result = es.search(index=indices, body=query)

    hits = [
        {
            "index": hit["_index"],
            "id": hit["_id"],
            **hit["_source"]
        }
        for hit in result["hits"]["hits"]
    ]

    return {
        "results": hits,
        "total": result["hits"]["total"]["value"]
    }