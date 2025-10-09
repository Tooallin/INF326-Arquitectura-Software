from .connection import get_client

from mensajes.mapping import index_name as index_messages, mapping as messages_mapping

def create_index(index_name: str, mapping: dict):
    es = get_client()

    # Crear el índice
    if es.indices.exists(index=index_name):
        print(f"⚠️  El índice '{index_name}' ya existe.")
        return

    es.indices.create(index=index_name, body=mapping, ignore=400)
    print(f"Índice {messages} creado ✅")

def create_all_indices():
    # Crear indice de mensaje
    create_index(index_name=index_messages, messages_mapping=messages_mapping)