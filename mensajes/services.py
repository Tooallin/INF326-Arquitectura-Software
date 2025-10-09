from mensajes.mapping import index_name
from elastic_search.connection import get_client
import json

def get_all(thread_id: int):
    es = get_client()

    query = {
        "query": {
            "match": {
                "thread_id": thread_id
            }
        }
    }

    resultado = es.search(index=index_name, body=query)

    # Extraer solo los documentos
    docs = [hit["_source"] for hit in resultado['hits']['hits']]

    # Convertir a JSON
    json_output = json.dumps(docs, indent=2)
    return json_output
