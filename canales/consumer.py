from canales.mapping import index_name
from elastic_search.connection import get_client

def create(body: dict):
    es = get_client()
    
    try:
        es.index(index=index_name, id=body["id"], document=body)
    except Exception as e:
        raise