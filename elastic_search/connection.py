from elasticsearch import Elasticsearch
import logging
import os

def get_client():
    """
    Crea y devuelve un cliente Elasticsearch conectado al servidor.
    """
    es = Elasticsearch(os.getenv("ELASTICSEARCH_URL"))

    if es.ping():
        logging.info("✅ Conectado a Elasticsearch")
    else:
        logging.error("❌ No se pudo conectar a Elasticsearch")

    return es