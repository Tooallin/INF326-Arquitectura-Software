# Nombre del indice para los canales en ElasticSearch
index_name = "channels"

# Mappings del indice canales
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "owner_id": {"type": "keyword"},
            "name": {"type": "text"},
            "users": {
                "type": "nested",
                "properties": {
                    "id": {"type": "keyword"},
                    "joined_at": {"type": "double"}
                }
            },
            "channel_type": {"type": "keyword"},
            "is_active": {"type": "boolean"},
            "created_at": { "type": "double" },
            "updated_at": { "type": "double" },
            "deleted_at": { "type": "double" }
        }
    }
}