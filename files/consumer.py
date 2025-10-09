from typing import Dict
from files.mapping import index_name
from elastic_search.connection import get_client
from elastic_search import ConflictError, NotFoundError, RequestError

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
	except ConflictError as e:
		# Ya existe un archivo con el mismo indice
		raise
	except (NotFoundError, RequestError):
		# Error de mapping, índice no existe, etc.
		raise
	except Exception:
		raise