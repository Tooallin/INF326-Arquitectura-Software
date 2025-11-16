from canales.mapping import index_name
from elastic_search.connection import get_client

def create(body: dict):
    es = get_client()
    
    channel_id = body.pop("id", None)
    try:
        es.index(index=index_name, id=channel_id, document=body)
    except Exception as e:
        raise

def update(body: dict):
    es = get_client()
    channel_id = body.pop("channel_id", None)
    if not channel_id:
        raise ValueError("El cuerpo debe incluir un campo 'id' para actualizar el documento.")

    try:
        es.update(
            index=index_name,
            id=channel_id,
            body={"doc": body}  # 👈 se actualizan solo los campos presentes
        )
    except Exception as e:
        raise

def delete(body: dict):
    """
    Elimina un mensaje existente en Elasticsearch.
    Requiere que body contenga el campo 'id'.
    """
    # es = get_client()
    # channel_id = body.get("id")
    # if not channel_id:
    #     raise ValueError("El cuerpo debe incluir un campo 'id' para eliminar el documento.")

    # try:
    #     es.delete(index=index_name, id=channel_id)
    # except Exception as e:
    #     raise

    es = get_client()
    channel_id = body.pop("channel_id", None)
    if not channel_id:
        raise ValueError("El cuerpo debe incluir un campo 'id' para actualizar el documento.")

    try:
        es.update(
            index=index_name,
            id=channel_id,
            body={"doc": body}  # 👈 se actualizan solo los campos presentes
        )
    except Exception as e:
        raise