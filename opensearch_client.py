from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=('admin', 'admin'),
    use_ssl=False
)

info = client.info()
print("Conexión exitosa:", info['version']['number'])

index_name = "personas"
index_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "nombre": {"type": "text"},
            "edad": {"type": "integer"},
            +"email": {"type": "keyword"}
        }
    }
}

if not client.indices.exist(index_name):
    client.indices.create(index=index_name, body=index_body)
    print(f"Índice '{index_name}' creado.")
else:
    print(f"Índice '{index_name}' ya existe.")

docs = [
    {"nombre": "José", "edad": 22, "email": "jose@mail.com"},
    {"nombre": "María", "edad": 30, "email": "maria@mail.com"},
    {"nombre": "Pedro", "edad": 28, "email": "pedro@mail.com"}
]

for i, doc in enumerate(docs, start=1):
    client.index(index=index_name, body=doc, id=i)

client.indices.refresh(index=index_name)
print("Documentos indexados.")

query = {
    "query": {
        "match":{
            "nombre": "José"
        }
    }
}

response = client.search(index=index_name, body=query)
print("Resultados búsqueda por nombre 'José':")
for hit in response['hits']['hits']:
    print(hit['_source'])


query_range = {
    "query": {
        "range": {
            "edad": {"gt": 25}
        }
    }
}

response_range = client.search(index=index_name, body=query_range)
print("\nResultados búsqueda edad > 25:")
for hit in response_range['hits']['hits']:
    print(hit['_source'])

#actualizar un documento
client.update(index=index_name, id=1, body={"doc": {"edad": 23}})
print("\nDocumento actualizado.")

#Eliminar un documento
client.delete(index=index_name, id=3)
print("Documento eliminado.")