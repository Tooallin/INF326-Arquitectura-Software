import json
from files.mapping import index_name
from elastic_search.connection import get_client
from elasticsearch import helpers

# Servicio para obtener todos los archivos indexados
def svc_getall():
	# Llamamos al cliente de ElasticSearch
	es = get_client()

	# Lista para almacenar todos nuestro archivos
	res_files = []

	# Obtenemos por lotes/hits todos los archivos
	for hit in helpers.scan(
		client=es,
		index=index_name,
		query={"query": {"match_all": {}}},
		_source=True,
		scroll="2m",
		size=1000
	):
		res_files.append(hit["_source"])

	# Convertimos a JSON nuestros resultados
	json_output = json.dumps(res_files, indent=2)

	# Retornamos los archivos
	return json_output

# Servicio para obtener archivo segun su id
def svc_getby_id(file_id: int):
	# Llamamos al cliente de ElasticSearch
	es = get_client()

	# Query para obtener el archivo por id
	query = {
		"query": {
			"match": {
				"id": file_id
			}
		}
	}

	# Buscamos nuestro archivo
	res_file = es.search(
		client=es,
		index=index_name,
		query=query
	)

	# Convertimos a JSON nuestros resultados
	json_output = json.dumps(res_file, indent=2)

	# Retornamos los archivos
	return json_output