from mensajes.indexation import index_name

def create(body: dict):
    try:
        es.index(index=index_name, id=body["id"], document=body)
    except Exception as e:
        raise