from threads.mapping import index_name
from elasticsearch import Elasticsearch
from elastic_search.connection import get_client
from datetime import datetime

client = get_client()



#client.indices.create(index=index_name, mappings=mappings)