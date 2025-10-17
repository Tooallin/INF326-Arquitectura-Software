from mensajes.mapping import index_name
from elastic_search.connection import get_client

def create(body: dict):
    es = get_client()
    
    try:
        es.index(index=index_name, id=body["id"], document=body)
    except Exception as e:
        raise

def update(body: dict):
    es = get_client()
    message_id = body.get("id")
    if not message_id:
        raise ValueError("El cuerpo debe incluir un campo 'id' para actualizar el documento.")

    try:
        es.update(
            index=index_name,
            id=message_id,
            body={"doc": body}  # 👈 se actualizan solo los campos presentes
        )
    except Exception as e:
        raise

def delete(body: dict):
    """
    Elimina un mensaje existente en Elasticsearch.
    Requiere que body contenga el campo 'id'.
    """
    es = get_client()
    message_id = body.get("id")
    if not message_id:
        raise ValueError("El cuerpo debe incluir un campo 'id' para eliminar el documento.")

    try:
        es.delete(index=index_name, id=message_id)
    except Exception as e:
        raise