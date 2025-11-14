index_name = "messages"

# Definir la estructura (mapping)
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},                     # UUID
            "thread_id": {"type": "keyword"},              # UUID
            "user_id": {"type": "keyword"},                # UUID
            "type": {"type": "keyword"},                   # enum text/audio/file
            "content": {"type": "text"},                   # texto libre
            "paths": {"type": "keyword"},                  # lista de strings
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
            "deleted_at": {"type": "date"},
        }
    }
}