index_name = "messages"

# Definir la estructura (mapping)
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "content": {"type": "text"},
            "author_id": {"type": "integer"},
            "thread_id": {"type": "integer"},
        }
    }
}