from fastapi import APIRouter, Query
from typing import List
from elasticsearch import Elasticsearch
from elastic_search.connection import get_client

router = APIRouter()

@router.get("/")
def search(
    q: str | None = Query(None, description="Texto a buscar (opcional)"),
    channel_id: int | None = Query(None),
    thread_id: int | None = Query(None),
    user_id: int | None = Query(None),
    index: List[str] | None = Query(["all"], description="Índices a consultar (puede ser una lista)"),
    limit: int = Query(10),
    offset: int = Query(0)
):
    es = get_client()  # tu función para obtener el cliente de Elasticsearch

    # Mapeo de nombres lógicos a índices reales en Elasticsearch
    index_map = {
        "message": "messages",
        "thread": "threads",
        "file": "files"
    }

    # === Determinar índices a buscar ===
    if "all" in index:
        indices = list(index_map.values())
    else:
        # Mapear cada valor recibido a su índice real, ignorando los no válidos
        indices = [index_map.get(i) for i in index if i in index_map]
        # Si ninguno fue válido, usar "messages" por defecto
        if not indices:
            indices = ["messages"]

    # === 🧩 Fase 1: buscar hilos si se filtra por canal ===
    thread_ids = []
    if channel_id:
        threads_query = {
            "query": {"term": {"channel_id": channel_id}},
            "_source": False,
            "size": 1000
        }
        threads_result = es.search(index="threads", body=threads_query)
        thread_ids = [hit["_id"] for hit in threads_result["hits"]["hits"]]

        if not thread_ids:
            return {"results": [], "total": 0}

    # === 🧩 Fase 2: construcción de filtros ===
    filters = []
    if thread_id:
        filters.append({"term": {"thread_id": thread_id}})
    if user_id:
        filters.append({"term": {"user_id": user_id}})
    if thread_ids:
        filters.append({"terms": {"thread_id": thread_ids}})

    # === 🧩 Fase 3: construcción de la query principal ===
    must_clauses = []
    if q:  # solo agregar búsqueda por texto si se proporciona `q`
        must_clauses.append({
            "multi_match": {
                "query": q,
                "fields": ["content", "title", "name", "description"],
                "fuzziness": "AUTO"
            }
        })

    query = {
        "query": {
            "bool": {
                "must": must_clauses,
                "filter": filters
            }
        },
        "from": offset,
        "size": limit
    }

    # === 🧩 Ejecución de la búsqueda ===
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
        "total": result["hits"]["total"]["value"],
        "results": hits
    }