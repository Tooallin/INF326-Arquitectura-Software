from elasticsearch import Elasticsearch, exceptions

from .connection import get_client
from mensajes.mapping import index_name as index_messages, mapping as messages_mapping

def create_index(index_name: str, mapping: dict):
    es = get_client()

    try:
        # Verificar si el índice ya existe
        if es.indices.exists(index=index_name):
            # Lanza una excepción si ya existe
            raise ValueError(f"El índice '{index_name}' ya existe.")

        # Crear el índice
        es.indices.create(index=index_name, body=mapping)

    except exceptions.ConnectionError as e:
        # Error de conexión con Elasticsearch
        raise ConnectionError(f"No se pudo conectar a Elasticsearch: {e}")

    except exceptions.RequestError as e:
        # Error al crear el índice (por ejemplo, mapping inválido)
        raise RuntimeError(f"Error al crear el índice '{index_name}': {e}")

def create_all_indices():
    # Crear indice de mensaje
    create_index(index_name=index_messages, mapping=messages_mapping)