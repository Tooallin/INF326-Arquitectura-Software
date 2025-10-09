from fastapi import APIRouter
from mensajes.services import get_all
from typing import List

router = APIRouter()

# Consultar en todos los indices
@router.get("/search")
def Search(
    q: str = Query(..., description="Palabra clave o frase a buscar"),
    channel_id: int | None = Query(None),
    thread_id: int | None = Query(None),
    user_id: int | None = Query(None),
    type: str | None = Query("all", description="message | thread | file | all"),
    limit: int = Query(10),
    offset: int = Query(0)
):
    es = get_client()

    # 🔹 Mapear el tipo a índices
    index_map = {
        "message": "messages",
        "thread": "threads",
        "file": "files"
    }

    # 🔹 Determinar los índices a consultar
    if type == "all":
        indices = list(index_map.values())
    else:
        indices = [index_map.get(type, "messages")]

    # 🔍 Construcción del query
    filters = []
    if channel_id:
        filters.append({"term": {"channel_id": channel_id}})
    if thread_id:
        filters.append({"term": {"thread_id": thread_id}})
    if user_id:
        filters.append({"term": {"user_id": user_id}})

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

    # 🔸 Buscar en múltiples índices a la vez
    result = es.search(index=indices, body=query)

    # 🔹 Formatear la respuesta
    hits = [
        {
            "index": hit["_index"],  # Saber de qué tipo viene
            "id": hit["_id"],
            **hit["_source"]
        }
        for hit in result["hits"]["hits"]
    ]

    return {
        "results": hits,
        "total": result["hits"]["total"]["value"]
    }