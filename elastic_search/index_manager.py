from .connection import get_client

def create_index(index_name: str, mapping: dict):
    es = get_client()

    # Crear el índice
    if es.indices.exists(index=index_name):
        print(f"⚠️  El índice '{index_name}' ya existe.")
        return

    es.indices.create(index=index_name, body=mapping, ignore=400)
    print(f"Índice {messages} creado ✅")