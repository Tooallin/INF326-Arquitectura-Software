import logging

from elastic_search.index_manager import create_all_indices
from .events import Receive

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # Crear indices para elastic search
    create_all_indices()

    # Comenzar a recibir de colas
    Receive()