from typing import Dict
from files.mapping import index_name
from elastic_search.connection import get_client

# Creamos un archivo en el indice "files"
def create_file(body: Dict[str, any]):
    # Llamamos al cliente de ElasticSearch
    es = get_client()

    file_id = body.pop("id", None)
    try:
        # Creamos/actualizamos un archivo
        res = es.index(
            index=index_name,
            id=file_id,
            document=body,
            op_type="create",
        )
        return res
    except Exception:
        raise

def delete_file(body: dict):
    """
    Elimina un archivo existente en Elasticsearch.
    Requiere que body contenga el campo 'id'.
    """

    es = get_client()
    file_id = body.pop("file_id", None)
    if not channel_id:
        raise ValueError("El cuerpo debe incluir un campo 'id' para actualizar el documento.")

    try:
        es.update(
            index=index_name,
            id=file_id,
            body={"doc": body}  # 👈 se actualizan solo los campos presentes
        )
    except Exception as e:
        raise