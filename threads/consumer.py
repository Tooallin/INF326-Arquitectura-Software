from threads.mapping import *
from elastic_search.connection import get_client
import json
import logging

def create_thread(body):
    client = get_client()
    try:
        client.index(
            index=index_name,
            id=body["id"],
            document=body
        )
    except Exception as e:
        logging.error(f"Error indexando hilo: {e}")


def update_thread(body):
    client = get_client()
    try:
        client.update(
            index=index_name,
            id=body["id"],
            doc=body
        )
    except Exception as e:
        logging.error(f"Error actualizando el hilo: {e}")

def delete_thread(body):
    client = get_client
    client.delete(index=index_name, id=body["id"])