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