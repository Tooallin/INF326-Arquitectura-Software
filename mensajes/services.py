from mensajes.mapping import index_name

def get_all(thread_id: int):
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
