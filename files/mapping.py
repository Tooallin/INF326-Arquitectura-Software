# Nombre del indice para los archivos en ElasticSearch
index_name = "files"

# Mappings del indice Files
mapping = {
	"mappings": {
		"properties": {
			"id": {"type": "integer"},
			"thread_id": {"type": "integer"},
			"message_id": {"type": "integer"},
			"name": {"type": "text"},
			"content": {"type": "text"},
			"pages": {"type": "integer"},
			"uploaded_at": {"type": "date"},
		}
	}
}