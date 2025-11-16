# Nombre del indice para los archivos en ElasticSearch
index_name = "files"

# Mappings del indice Files
mapping = {
	"mappings": {
		"properties": {
			"id": {
				"type": "keyword"
			},
			"filename": {
				"type": "text",
				"fields": {
					"raw": { "type": "keyword" }
				}
			},
			"mime_type": {
				"type": "keyword"
			},
			"size": {
				"type": "integer"
			},
			"bucket": {
				"type": "keyword"
			},
			"object_key": {
				"type": "keyword"
			},
			"message_id": {
				"type": "keyword"
			},
			"thread_id": {
				"type": "keyword"
			},
			"checksum_sha256": {
				"type": "keyword"
			},
			"created_at": {
				"type": "date"
			},
			"deleted_at": {
				"type": "date"
			}
		}
	}
}