# Nombre del indice para los archivos en ElasticSearch
index_name = "channels"

# Mappings del indice Files
mapping = {
	"mappings": {
		"properties": {
			"id": {"type": "integer"},
			"title": {"type": "integer"},
			"created_at": {"type": "date"},
		}
	}
}