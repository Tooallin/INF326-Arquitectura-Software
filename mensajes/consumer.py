from mensajes.indexation import index_name

def create(body: dict):
    es.index(index=index_name, id=body["id"], document=body)