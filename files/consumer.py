from typing import Dict
from files.mapping import index_name
from elastic_search.connection import get_client

# Creamos un archivo en el indice "files"
def create_file(body: Dict[str, any]):
	# Llamamos al cliente de ElasticSearch
	es = get_client()

	try:
		# Creamos/actualizamos un archivo
		res = es.index(
			index=index_name,
			id=body["id"],
			document=body,
			op_type="create",
		)
		return res
	except Exception:
		raise