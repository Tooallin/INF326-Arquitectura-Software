index_name = "threads"

#Definir la estructura
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},                  # string UUID → keyword
            "channel_id": {"type": "keyword"},          # FK → keyword
            "title": {"type": "text"},                  # búsquedas por texto completo
            "created_by": {"type": "keyword"},          # ID de usuario -> keyword
            "status": {"type": "keyword"},              # enum: open / archived
            "meta": {"type": "object"},                 # JSON arbitrario
            "created_at": {"type": "date"},             # ISO8601 → date
            "updated_at": {"type": "date"},
            "deleted_at": {"type": "date"},
        }
    }
}