from elasticsearch import Elasticsearch
import logging

def get_client():
    """
    Crea y devuelve un cliente Elasticsearch conectado al servidor.
    """
    es = Elasticsearch("http://localhost:9200")

    if es.ping():
        logging.info("✅ Conectado a Elasticsearch")
    else:
        logging.error("❌ No se pudo conectar a Elasticsearch")

    return es