from fastapi import APIRouter, Query
from typing import List
from elasticsearch import Elasticsearch
from elastic_search.connection import get_client

from enum import Enum

class IndexEnum(str, Enum):
    all = "all"
    messages = "messages"
    threads = "threads"
    files = "files"

router = APIRouter()

@router.get("/")
def search(
    q: str | None = Query(None, description="Texto a buscar (opcional)"),
    channel_id: int | None = Query(None),
    thread_id: int | None = Query(None),
    author_id: int | None = Query(None),
    index: List[IndexEnum] = Query(
        ["all"],
        description="Índices a consultar (puede ser una lista: 'all', 'messages', 'threads', 'files', 'channels')"
    ),
    limit: int = Query(10),
    offset: int = Query(0)
):
    es = get_client() 

    # Array de índices válidos
    valid_indices = ["messages", "threads", "files", "channels"]
    index_aux = [i.value for i in index]
    '''
    print("--------------------------------")
    print(index_aux)
    print("--------------------------------")
    '''
    indices = index_aux

    # Si quedó vacía, usar todos los índices válidos
    if "all" in index_aux or not index_aux:
        indices = valid_indices
    '''
    print("--------------------------------")
    print(indices)
    print("--------------------------------")
    '''
    filters = []
    # === 🧩 Fase 1: buscar hilos si se filtra por canal ===
    thread_ids = []
    if channel_id:
        if "channels" in indices:
            # Filtro especial: buscar por _id en threads
            filters.append({
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must": [
                                    {"ids": {"values": [str(channel_id)]}},   # _id igual a thread_id
                                    {"term": {"_index": "channels"}}         # solo en el índice channels
                                ]
                            }
                        },
                        {
                            "bool": {
                                "must_not": {
                                    "term": {"_index": "channels"}          # otros índices pasan
                                }
                            }
                        }
                    ]
                }
            })
        else:
            threads_query = {
                "query": {"term": {"channel_id": channel_id}},
                "_source": False,
                "size": 1000
            }
            threads_result = es.search(index="threads", body=threads_query)
            thread_ids = [int(hit["_id"]) for hit in threads_result["hits"]["hits"]]
        
            '''
            if not thread_ids:
                return {"results": [], "total": 0}
            '''
    '''
    print(thread_ids)
    '''
    # === 🧩 Fase 2: construcción de filtros ===
    
    if thread_id:
        if "threads" in indices:
            # Filtro especial: buscar por _id en threads
            filters.append({
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must": [
                                    {"ids": {"values": [str(thread_id)]}},   # _id igual a thread_id
                                    {"term": {"_index": "threads"}}         # solo en el índice threads
                                ]
                            }
                        },
                        {
                            "bool": {
                                "must_not": {
                                    "term": {"_index": "threads"}          # otros índices pasan
                                }
                            }
                        }
                    ]
                }
            })
        else:
            # Búsqueda normal por thread_id
            filters.append({"term": {"thread_id": thread_id}})
    if author_id:
        filters.append({"term": {"author_id": author_id}})
    if thread_ids:
        filters.append({"terms": {"thread_id": thread_ids}})
    '''
    print(filters)
    '''
    # === 🧩 Fase 3: construcción de la query principal ===
    must_clauses = []
    if q:  # solo agregar búsqueda por texto si se proporciona `q`
        must_clauses.append({
            "multi_match": {
                "query": q,
                "fields": ["content", "title", "name", "category", "tags"],
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
    '''
    print(query)
    '''
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