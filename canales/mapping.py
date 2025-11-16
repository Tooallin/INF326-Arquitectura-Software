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
                    "joined_at": {"type": "date", "format": "epoch_second"}
                }
            },
            "channel_type": {"type": "keyword"},
            "is_active": {"type": "boolean"},
            "created_at": {"type": "date", "format": "epoch_second"},
            "updated_at": {"type": "date", "format": "epoch_second"},
            "deleted_at": {"type": "date", "format": "epoch_second"}
        }
    }
}