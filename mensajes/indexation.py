from elastic_search.connection import get_client

def create_index():
    es = get_client()

    index_name = "messages"

    # Definir la estructura (mapping)
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "content": {"type": "text"},
                "thread_id": {"type": "integer"},
            }
        }
    }

    # Crear el índice
    if es.indices.exists(index=index_name):
        print(f"⚠️  El índice '{index_name}' ya existe.")
        return

    es.indices.create(index=index_name, body=mapping, ignore=400)
    print(f"Índice {messages} creado ✅")