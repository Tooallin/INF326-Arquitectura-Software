from threads.mapping import *
from elastic_search.connection import get_client
import json
import logging

def create_thread(body):
    client = get_client()
    thread_id = body.pop("id", None)
    try:
        client.index(
            index=index_name,
            id=thread_id,
            document=body
        )
    except Exception as e:
        logging.error(f"Error indexando hilo: {e}")


def update_thread(body):
    client = get_client()
    thread_id = body.pop("id", None)
    try:
        client.update(
            index=index_name,
            id=thread_id,
            doc=body
        )
    except Exception as e:
        logging.error(f"Error actualizando el hilo: {e}")

def delete_thread(body):
    client = get_client()
    thread_id = body.pop("id", None)
    try:
        client.update(
            index=index_name,
            id=thread_id,
            doc=body
        )
    except Exception as e:
        logging.error(f"Error borrando el hilo: {e}")