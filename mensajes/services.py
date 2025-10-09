from mensajes.mapping import index_name
from elastic_search.connection import get_client
import json

def search_message(
	q: str,
	author_id: int | None,
	thread_id: int | None,
	limit: int,
	offset: int
):
    es = get_client()

    # 🔍 Construcción del query base
    filters = []
    if author_id:
        filters.append({"term": {"author_id": author_id}})
    if thread_id:
        filters.append({"term": {"thread_id": thread_id}})

    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"content": q}}  # búsqueda textual
                ],
                "filter": filters
            }
        },
        "sort": [{"sent_at": {"order": "desc"}}],
        "from": offset,
        "size": limit
    }

    # 🔸 Ejecutar la búsqueda
    result = es.search(index=index_name, body=query)

    # 🔹 Formatear resultados
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
